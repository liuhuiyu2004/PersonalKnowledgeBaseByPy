// 网络爬虫组件
// @author LiuHuiYu
const WebCrawler = {
    template: `
        <div class="web-crawler">
            <el-card>
                <h2>🌐 网络采集</h2>
                
                <el-tabs v-model="activeTab">
                    <!-- 网页抓取 -->
                    <el-tab-pane label="网页抓取" name="fetch">
                        <el-form :model="fetchForm" label-width="100px" style="margin-top: 20px;">
                            <el-form-item label="网页 URL">
                                <el-input 
                                    v-model="fetchForm.url" 
                                    placeholder="请输入要抓取的网页 URL"
                                    clearable
                                >
                                    <template #append>
                                        <el-button @click="previewUrl">🔍 导入预览</el-button>
                                    </template>
                                </el-input>
                            </el-form-item>
                            
                            <el-form-item label="选项">
                                <el-checkbox v-model="fetchForm.auto_save">自动保存到知识库</el-checkbox>
                                <el-checkbox v-model="fetchForm.generate_summary">AI 生成摘要</el-checkbox>
                            </el-form-item>
                            
                            <el-form-item>
                                <el-button type="primary" @click="fetchPage" :loading="fetching">
                                    🕷️ 开始抓取
                                </el-button>
                            </el-form-item>
                        </el-form>
                    </el-tab-pane>
                    
                    <!-- 网络搜索 -->
                    <el-tab-pane label="网络搜索" name="search">
                        <el-form :model="searchForm" label-width="100px" style="margin-top: 20px;">
                            <el-form-item label="搜索关键词">
                                <el-input 
                                    v-model="searchForm.query" 
                                    placeholder="输入要搜索的关键词"
                                    clearable
                                ></el-input>
                            </el-form-item>
                            
                            <el-form-item label="搜索引擎">
                                <el-select v-model="searchForm.engine" placeholder="选择搜索引擎" style="width: 100%;">
                                    <el-option
                                        v-for="item in searchEngines"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value"
                                    >
                                        <span style="float: left">{{ item.label }}</span>
                                        <span style="float: right; color: #8492a6; font-size: 13px">{{ item.desc }}</span>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            
                            <el-form-item label="结果数量">
                                <el-input-number v-model="searchForm.num_results" :min="1" :max="10" />
                            </el-form-item>
                            
                            <el-form-item label="选项">
                                <el-checkbox v-model="searchForm.auto_save">自动保存结果到知识库</el-checkbox>
                            </el-form-item>
                            
                            <el-form-item>
                                <el-button type="primary" @click="searchWeb" :loading="searching">
                                    🔍 开始搜索
                                </el-button>
                            </el-form-item>
                        </el-form>
                    </el-tab-pane>
                </el-tabs>
            </el-card>
            
            <!-- 导入预览对话框 -->
            <el-dialog v-model="previewDialogVisible" title="📋 网页预览与分析" width="80%" top="5vh">
                <el-descriptions :column="2" border v-loading="previewLoading">
                    <el-descriptions-item label="标题">{{ previewData.title }}</el-descriptions-item>
                    <el-descriptions-item label="URL">{{ previewData.url }}</el-descriptions-item>
                    <el-descriptions-item label="AI 摘要" :span="2">
                        <el-tag type="success" effect="plain">✨ Agent 生成</el-tag>
                        <div style="margin-top: 8px;">{{ previewData.summary }}</div>
                    </el-descriptions-item>
                    <el-descriptions-item label="建议标签" :span="2">
                        <el-tag v-for="tag in previewData.suggested_tags" :key="tag" style="margin-right: 5px;">
                            🏷️ {{ tag }}
                        </el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="推荐分类" :span="2">
                        <el-tag type="warning" effect="plain" v-if="previewData.category">
                            📁 {{ previewData.category }}
                        </el-tag>
                        <span v-else style="color: #999;">暂无匹配分类</span>
                    </el-descriptions-item>
                </el-descriptions>
                
                <el-divider />
                
                <div style="margin-top: 15px;">
                    <h4>📄 内容预览（富文本）</h4>
                    <div class="content-preview" style="max-height: 400px; overflow-y: auto; border: 1px solid #e0e0e0; padding: 15px; background: #fafafa;">
                        <div v-html="previewData.html_content || previewData.content"></div>
                    </div>
                </div>
                
                <template #footer>
                    <span class="dialog-footer">
                        <el-button @click="previewDialogVisible = false">取消</el-button>
                        <el-button type="primary" @click="savePreview" :loading="saving">
                            💾 保存到知识库
                        </el-button>
                    </span>
                </template>
            </el-dialog>
            
            <!-- 抓取结果预览 -->
            <el-card v-if="fetchResult" style="margin-top: 20px;">
                <template #header>
                    <div class="card-header">
                        <span>抓取结果预览</span>
                        <el-button size="small" type="success" @click="saveResult">💾 保存到知识库</el-button>
                    </div>
                </template>
                
                <el-descriptions :column="2" border>
                    <el-descriptions-item label="标题">{{ fetchResult.title }}</el-descriptions-item>
                    <el-descriptions-item label="URL">{{ fetchResult.url }}</el-descriptions-item>
                    <el-descriptions-item label="内容长度">{{ fetchResult.content?.length || 0 }} 字符</el-descriptions-item>
                </el-descriptions>
                
                <div class="content-preview" style="margin-top: 10px;">{{ fetchResult.content }}</div>
            </el-card>
            
            <!-- 搜索结果 -->
            <el-card v-if="searchResults && searchResults.length > 0" style="margin-top: 20px;">
                <template #header>
                    <span>搜索结果 ({{ searchResults.length }})</span>
                </template>
                
                <el-table :data="searchResults" stripe style="width: 100%">
                    <el-table-column prop="title" label="标题" show-overflow-tooltip />
                    <el-table-column prop="snippet" label="摘要" show-overflow-tooltip />
                    <el-table-column prop="url" label="URL" show-overflow-tooltip width="300" />
                    <el-table-column label="操作" width="150">
                        <template #default="scope">
                            <el-button size="small" @click="previewSearchResultWithAgent(scope.row)">🔍 导入预览</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-card>
        </div>
    `,
    
    data() {
        return {
            activeTab: 'fetch',
            fetchForm: {
                url: '',
                auto_save: true,
                generate_summary: true
            },
            searchForm: {
                query: '',
                engine: 'bing', // 默认使用 Bing
                num_results: 5,
                auto_save: false
            },
            searchEngines: [
                {
                    value: 'duckduckgo',
                    label: 'DuckDuckGo',
                    desc: '隐私保护'
                },
                {
                    value: 'bing',
                    label: 'Bing 必应',
                    desc: '中文友好'
                }
            ],
            fetching: false,
            searching: false,
            fetchResult: null,
            searchResults: null,
            // 新增：预览对话框相关
            previewDialogVisible: false,
            previewLoading: false,
            saving: false,
            previewData: {
                title: '',
                url: '',
                content: '',
                html_content: '',
                summary: '',
                suggested_tags: [],
                category: null
            }
        }
    },
    
    methods: {
        async fetchPage() {
            if (!this.fetchForm.url) {
                ElementPlus.ElMessage.warning('请输入 URL');
                return;
            }
            
            this.fetching = true;
            try {
                const response = await axios.post('/api/web/fetch', this.fetchForm);
                this.fetchResult = response.data;
                
                if (this.fetchForm.auto_save) {
                    ElementPlus.ElMessage.success('已保存到知识库');
                    this.$emit('saved');
                } else {
                    ElementPlus.ElMessage.success('抓取成功');
                }
            } catch (error) {
                // 显示详细错误信息
                let errorMsg = '抓取失败：';
                if (error.response) {
                    // 后端返回了错误
                    errorMsg += error.response.data?.detail || error.response.data?.message || `HTTP ${error.response.status}`;
                } else if (error.message) {
                    // 网络错误或其他错误
                    errorMsg += error.message;
                }
                
                ElementPlus.ElMessage.error(errorMsg);
                console.error('Fetch error:', error);
            } finally {
                this.fetching = false;
            }
        },
        
        async searchWeb() {
            if (!this.searchForm.query) {
                ElementPlus.ElMessage.warning('请输入搜索关键词');
                return;
            }
            
            this.searching = true;
            try {
                const response = await axios.post('/api/web/search', this.searchForm);
                this.searchResults = response.data;
                
                if (this.searchForm.auto_save && this.searchResults.length > 0) {
                    ElementPlus.ElMessage.success(`搜索完成，已保存 ${Math.min(3, this.searchResults.length)} 条结果`);
                    this.$emit('saved');
                } else {
                    ElementPlus.ElMessage.success(`找到 ${this.searchResults.length} 条结果`);
                }
            } catch (error) {
                ElementPlus.ElMessage.error('搜索失败');
                console.error('Search error:', error);
            } finally {
                this.searching = false;
            }
        },
        
        saveResult() {
            if (this.fetchResult) {
                // 已经在抓取时保存了
                ElementPlus.ElMessage.info('结果已保存');
            }
        },
        
        previewSearchResult(result) {
            const { h } = Vue;
            
            ElementPlus.ElMessageBox.alert(
                h('div', [
                    h('a', {
                        href: result.url,
                        target: '_blank',
                        rel: 'noopener noreferrer',
                        style: 'color: #409EFF; text-decoration: none; font-size: 14px; display: block; margin-bottom: 10px; word-break: break-all;'
                    }, result.url),
                    h('div', {
                        style: 'white-space: pre-wrap; line-height: 1.6; margin-top: 15px; max-height: 400px; overflow-y: auto;'
                    }, result.snippet)
                ]),
                result.title || '搜索结果预览',
                {
                    dangerouslyUseHTMLString: true,
                    confirmButtonText: '关闭',
                    width: '80%',
                    customStyle: {
                        maxWidth: '1200px'
                    }
                }
            );
        },
        
        // 新增：使用 agent 分析搜索结果
        async previewSearchResultWithAgent(result) {
            console.log('[PreviewSearchResultWithAgent] 开始分析:', result);
            
            // 重置预览数据
            this.previewData = {
                title: '',
                url: '',
                content: '',
                html_content: '',
                summary: '',
                suggested_tags: [],
                category: null
            };
            
            if (!result.url) {
                ElementPlus.ElMessage.warning('该结果没有 URL，无法分析');
                // 降级显示基本信息
                this.previewData = {
                    title: result.title || '搜索结果',
                    url: result.url || '',
                    content: result.snippet || '',
                    html_content: result.snippet || '',
                    summary: result.snippet || '',
                    suggested_tags: [],
                    category: null
                };
                this.previewDialogVisible = true;
                return;
            }
            
            this.previewLoading = true;
            this.previewDialogVisible = true;
            
            try {
                console.log('[PreviewSearchResultWithAgent] 开始分析 URL:', result.url);
                const response = await axios.post('/api/web/preview', {
                    url: result.url
                });
                
                console.log('[PreviewSearchResultWithAgent] 分析结果:', response.data);
                this.previewData = response.data;
                
                ElementPlus.ElMessage.success('分析完成');
            } catch (error) {
                console.error('[PreviewSearchResultWithAgent] 分析失败:', error);
                let errorMsg = '分析失败：';
                if (error.response) {
                    errorMsg += error.response.data?.detail || error.response.data?.message || `HTTP ${error.response.status}`;
                } else if (error.message) {
                    errorMsg += error.message;
                }
                
                ElementPlus.ElMessage.error(errorMsg);
                
                // 降级显示基本信息
                this.previewData = {
                    title: result.title || '搜索结果',
                    url: result.url || '',
                    content: result.snippet || '',
                    html_content: result.snippet || '',
                    summary: result.snippet || '',
                    suggested_tags: [],
                    category: null
                };
            } finally {
                this.previewLoading = false;
            }
        },
        
        // 新增：预览 URL
        async previewUrl() {
            if (!this.fetchForm.url) {
                ElementPlus.ElMessage.warning('请输入 URL');
                return;
            }
            
            // 重置预览数据
            this.previewData = {
                title: '',
                url: '',
                content: '',
                html_content: '',
                summary: '',
                suggested_tags: [],
                category: null
            };
            
            this.previewLoading = true;
            this.previewDialogVisible = true;
            
            try {
                const response = await axios.post('/api/web/preview', {
                    url: this.fetchForm.url
                });
                
                this.previewData = response.data;
                
                ElementPlus.ElMessage.success('分析完成');
            } catch (error) {
                let errorMsg = '分析失败：';
                if (error.response) {
                    errorMsg += error.response.data?.detail || error.response.data?.message || `HTTP ${error.response.status}`;
                } else if (error.message) {
                    errorMsg += error.message;
                }
                
                ElementPlus.ElMessage.error(errorMsg);
                console.error('Preview error:', error);
                this.previewDialogVisible = false;
            } finally {
                this.previewLoading = false;
            }
        },
        
        // 新增：保存预览结果
        async savePreview() {
            if (!this.previewData.url) {
                ElementPlus.ElMessage.warning('没有可保存的内容');
                return;
            }
            
            this.saving = true;
            
            try {
                // 构建保存数据
                const saveData = {
                    title: this.previewData.title,
                    content: this.previewData.html_content || this.previewData.content,
                    summary: this.previewData.summary,
                    source_type: 'web',
                    source_url: this.previewData.url,
                    tag_ids: []  // TODO: 可以根据 suggested_tags 和 category 自动匹配标签
                };
                
                const response = await axios.post('/api/knowledge/', saveData);
                
                ElementPlus.ElMessage.success('保存成功');
                this.previewDialogVisible = false;
                this.$emit('saved');
                
                // 清空预览数据
                this.previewData = {
                    title: '',
                    url: '',
                    content: '',
                    html_content: '',
                    summary: '',
                    suggested_tags: [],
                    category: null
                };
            } catch (error) {
                let errorMsg = '保存失败：';
                if (error.response) {
                    errorMsg += error.response.data?.detail || error.response.data?.message;
                } else if (error.message) {
                    errorMsg += error.message;
                }
                
                ElementPlus.ElMessage.error(errorMsg);
                console.error('Save error:', error);
            } finally {
                this.saving = false;
            }
        },

    }
};

// 导出组件
if (typeof window !== 'undefined') {
    window.WebCrawler = WebCrawler;
}
