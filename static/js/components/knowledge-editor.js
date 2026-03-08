// 知识编辑器组件
// @author LiuHuiYu
const KnowledgeEditor = {
    props: ['editData'],
    
    template: `
        <div class="editor-container">
            <h2>{{ isEdit ? '编辑知识' : '新建知识' }}</h2>
            
            <el-form :model="form" :rules="rules" ref="formRef" label-width="80px" style="margin-top: 20px;">
                <el-form-item label="标题" prop="title">
                    <el-input v-model="form.title" placeholder="请输入标题" clearable></el-input>
                </el-form-item>
                
                <el-form-item label="内容" prop="content">
                    <div ref="editorRef" style="border: 1px solid #dcdfe6; z-index: 100;">
                        <toolbar
                            style="border-bottom: 1px solid #dcdfe6"
                            :editor="editor"
                            :defaultConfig="toolbarConfig"
                        ></toolbar>
                        <editor
                            style="height: 400px; overflow-y: hidden;"
                            v-model="form.content"
                            :defaultConfig="editorConfig"
                        ></editor>
                    </div>
                </el-form-item>
                
                <el-form-item label="来源 URL" prop="source_url">
                    <el-input v-model="form.source_url" placeholder="可选，如果是网页来源请填写" clearable></el-input>
                </el-form-item>
                
                <el-form-item label="标签">
                    <el-select 
                        v-model="form.tag_ids" 
                        multiple 
                        filterable 
                        allow-create 
                        default-first-option
                        placeholder="选择或创建标签"
                        style="width: 100%;"
                        @change="handleTagChange"
                    >
                        <el-option
                            v-for="tag in allTags"
                            :key="tag.id"
                            :label="tag.name"
                            :value="tag.id"
                        >
                            <span style="float: left">{{ tag.name }}</span>
                            <span style="float: right; color: #8492a6; font-size: 13px">
                                <el-tag size="small" :color="tag.color" effect="plain"></el-tag>
                            </span>
                        </el-option>
                    </el-select>
                </el-form-item>
                
                <el-form-item label="摘要">
                    <el-input 
                        v-model="form.summary" 
                        type="textarea" 
                        :rows="3" 
                        placeholder="可选，或使用 AI 自动生成"
                    ></el-input>
                    <el-button size="small" @click="autoSummarize" :loading="summarizing" style="margin-top: 10px;">
                        🤖 AI 生成摘要
                    </el-button>
                </el-form-item>
                
                <el-form-item>
                    <el-button type="primary" @click="submitForm" :loading="saving">保存</el-button>
                    <el-button @click="cancel">取消</el-button>
                </el-form-item>
            </el-form>
        </div>
    `,
    
    data() {
        return {
            form: {
                title: '',
                content: '',
                source_url: '',
                summary: '',
                tag_ids: []
            },
            rules: {
                title: [
                    { required: true, message: '请输入标题', trigger: 'blur' },
                    { min: 1, max: 500, message: '长度在 1 到 500 个字符', trigger: 'blur' }
                ],
                content: [
                    { required: true, message: '请输入内容', trigger: 'blur' }
                ]
            },
            allTags: [],
            saving: false,
            summarizing: false,
            isEdit: false,
            // 富文本编辑器
            editor: null,
            editorRef: null,
            toolbarConfig: {},
            editorConfig: { 
                placeholder: '请输入内容，支持富文本格式（加粗、斜体、链接、列表等）...',
                MENU_CONF: {
                    uploadImage: {
                        maxFileSize: 10 * 1024 * 1024, // 10MB
                        allowedFileTypes: ['image/*']
                    }
                }
            }
        }
    },
    
    async created() {
        console.log('Editor created, editData:', this.editData);
        await this.fetchTags();
        console.log('Tags loaded:', this.allTags);
        if (this.editData) {
            this.isEdit = true;
            const tagIds = this.editData.tags ? this.editData.tags.map(t => {
                console.log('Tag object:', t);
                return t.id;
            }) : [];
            this.form = {
                title: this.editData.title || '',
                content: this.editData.content || '',
                source_url: this.editData.source_url || '',
                summary: this.editData.summary || '',
                tag_ids: tagIds
            };
            console.log('Edit form initialized with tag_ids:', this.form.tag_ids);
        }
    },
    
    mounted() {
        // 初始化富文本编辑器
        this.$nextTick(() => {
            this.initEditor();
        });
    },
    
    beforeUnmount() {
        // 销毁编辑器实例
        if (this.editor) {
            this.editor.destroy();
        }
    },
    
    methods: {
        initEditor() {
            // 创建编辑器
            const { createEditor, createToolbar } = window.wangEditor;
            
            this.editor = createEditor({
                selector: this.$refs.editorRef.querySelector('editor'),
                html: this.form.content,
                config: this.editorConfig,
                mode: 'default',
            })
            
            // 创建工具栏
            const toolbar = createToolbar({
                editor: this.editor,
                selector: this.$refs.editorRef.querySelector('toolbar'),
                config: this.toolbarConfig,
                mode: 'default',
            })
            
            console.log('富文本编辑器初始化完成');
        },
        
        async fetchTags() {
            try {
                const response = await axios.get('/api/tags/');
                console.log('Fetched tags response:', response.data);
                this.allTags = response.data;
                console.log('allTags set to:', this.allTags);
            } catch (error) {
                console.error('Failed to fetch tags:', error);
                ElementPlus.ElMessage.error('加载标签失败');
            }
        },
        
        async handleTagChange(selectedValues) {
            // 检查是否有新创建的标签 (字符串类型，不是数字 ID)
            const newTags = selectedValues.filter(val => typeof val === 'string');
            
            if (newTags.length > 0) {
                // 创建新标签
                for (const tagName of newTags) {
                    try {
                        const response = await axios.post('/api/tags/', {
                            name: tagName,
                            color: '#' + Math.floor(Math.random()*16777215).toString(16) // 随机颜色
                        });
                        
                        // 刷新标签列表
                        await this.fetchTags();
                        
                        // 更新 form.tag_ids，用新标签的 ID 替换字符串
                        const newTagId = response.data.id;
                        const index = this.form.tag_ids.indexOf(tagName);
                        if (index > -1) {
                            this.form.tag_ids.splice(index, 1, newTagId);
                        }
                        
                        ElementPlus.ElMessage.success(`标签 "${tagName}" 已创建`);
                    } catch (error) {
                        console.error('Create tag error:', error);
                        // 如果创建失败，从选择中移除
                        const index = this.form.tag_ids.indexOf(tagName);
                        if (index > -1) {
                            this.form.tag_ids.splice(index, 1);
                        }
                        ElementPlus.ElMessage.error(`创建标签 "${tagName}" 失败`);
                    }
                }
            }
        },
        
        async autoSummarize() {
            if (!this.form.content) {
                ElementPlus.ElMessage.warning('请先输入内容');
                return;
            }
            
            this.summarizing = true;
            try {
                const response = await axios.post('/api/ai/summarize', {
                    text: this.form.content,
                    max_length: 200
                });
                
                if (response.data.success) {
                    this.form.summary = response.data.summary;
                    ElementPlus.ElMessage.success('摘要生成成功');
                }
            } catch (error) {
                ElementPlus.ElMessage.error('生成失败，请手动输入');
                console.error('Summarize error:', error);
            } finally {
                this.summarizing = false;
            }
        },
        
        async submitForm() {
            try {
                await this.$refs.formRef.validate();
                
                this.saving = true;
                
                // 确保 tag_ids 是数字数组 - 过滤掉所有非数字的值
                let tagIds = [];
                if (this.form.tag_ids && Array.isArray(this.form.tag_ids)) {
                    tagIds = this.form.tag_ids
                        .filter(id => id !== null && id !== undefined && id !== '')
                        .map(id => {
                            const num = parseInt(id);
                            return isNaN(num) ? null : num;
                        })
                        .filter(num => num !== null);
                }
                
                console.log('Submitting with tag_ids:', tagIds);
                
                const data = {
                    title: this.form.title,
                    content: this.form.content,
                    summary: this.form.summary,
                    source_type: this.form.source_url ? 'web' : 'manual',
                    source_url: this.form.source_url,
                    tag_ids: tagIds
                };
                
                if (this.isEdit) {
                    // 更新
                    await axios.put(`/api/knowledge/${this.editData.id}`, data);
                } else {
                    // 创建
                    await axios.post('/api/knowledge/', data);
                }
                
                ElementPlus.ElMessage.success('保存成功');
                this.$emit('saved');
            } catch (error) {
                if (error !== 'cancel') {
                    // 提取详细错误信息
                    let errorMsg = '保存失败';
                    if (error.response) {
                        // 服务器返回错误
                        const detail = error.response.data.detail;
                        if (typeof detail === 'string') {
                            errorMsg = detail;
                        } else if (Array.isArray(detail)) {
                            // 422 验证错误，显示所有错误
                            errorMsg = detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join(', ');
                        } else if (detail && typeof detail === 'object') {
                            errorMsg = JSON.stringify(detail);
                        }
                    } else if (error.message) {
                        errorMsg = error.message;
                    }
                    ElementPlus.ElMessage.error(errorMsg);
                    console.error('Save error:', error);
                }
            } finally {
                this.saving = false;
            }
        },
        
        cancel() {
            this.$emit('cancel');
        }
    }
};

// 导出组件
if (typeof window !== 'undefined') {
    window.KnowledgeEditor = KnowledgeEditor;
}
