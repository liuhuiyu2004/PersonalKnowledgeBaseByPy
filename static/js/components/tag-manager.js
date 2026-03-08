// 标签管理组件
// @author LiuHuiYu
const TagManager = {
    template: `
        <div class="tag-manager">
            <el-card>
                <h2>🏷️ 标签管理</h2>
                
                <!-- 添加标签表单 -->
                <el-form :inline="true" :model="form" class="tag-form">
                    <el-form-item label="标签名称">
                        <el-input 
                            v-model="form.name" 
                            placeholder="输入标签名称"
                            style="width: 200px;"
                        ></el-input>
                    </el-form-item>
                    
                    <el-form-item label="颜色">
                        <el-color-picker v-model="form.color"></el-color-picker>
                    </el-form-item>
                    
                    <el-form-item>
                        <el-button type="primary" @click="addTag" :loading="adding">添加标签</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
            
            <!-- 标签列表 -->
            <el-card style="margin-top: 20px;">
                <template #header>
                    <div class="card-header">
                        <span>所有标签</span>
                        <el-button size="small" @click="refreshTags">🔄 刷新</el-button>
                    </div>
                </template>
                
                <div v-if="loading" class="loading-container">
                    <el-skeleton :rows="5" animated />
                </div>
                
                <div v-else-if="tags.length === 0" class="empty-state">
                    <i>🏷️</i>
                    <h3>暂无标签</h3>
                    <p>点击上方表单添加第一个标签</p>
                </div>
                
                <el-table v-else :data="tags" style="width: 100%">
                    <el-table-column prop="name" label="标签名称" width="200">
                        <template #default="{ row }">
                            <el-tag :color="row.color" effect="plain" size="large">
                                {{ row.name }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    
                    <el-table-column prop="color" label="颜色" width="150">
                        <template #default="{ row }">
                            <el-color-picker v-model="row.color" disabled></el-color-picker>
                            <span style="margin-left: 10px; font-size: 12px;">{{ row.color }}</span>
                        </template>
                    </el-table-column>
                    
                    <el-table-column prop="created_at" label="创建时间">
                        <template #default="{ row }">
                            {{ formatDate(row.created_at) }}
                        </template>
                    </el-table-column>
                    
                    <el-table-column label="操作" width="200" fixed="right">
                        <template #default="{ row }">
                            <el-button 
                                size="small" 
                                type="primary"
                                @click="editTag(row)"
                            >
                                编辑
                            </el-button>
                            <el-button 
                                size="small" 
                                type="danger" 
                                @click="deleteTag(row.id)"
                                :loading="deletingId === row.id"
                            >
                                删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-card>
            
            <!-- 编辑标签对话框 -->
            <el-dialog 
                v-model="editDialogVisible" 
                title="编辑标签" 
                width="400px"
            >
                <el-form :model="editForm" label-width="80px">
                    <el-form-item label="标签名称">
                        <el-input v-model="editForm.name" placeholder="输入标签名称"></el-input>
                    </el-form-item>
                    <el-form-item label="颜色">
                        <el-color-picker v-model="editForm.color"></el-color-picker>
                    </el-form-item>
                </el-form>
                <template #footer>
                    <el-button @click="editDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="updateTag" :loading="updating">确定</el-button>
                </template>
            </el-dialog>
        </div>
    `,
    
    data() {
        return {
            form: {
                name: '',
                color: '#3498db'
            },
            tags: [],
            loading: false,
            adding: false,
            deletingId: null,
            // 编辑对话框
            editDialogVisible: false,
            editForm: {
                id: null,
                name: '',
                color: ''
            },
            updating: false
        }
    },
    
    created() {
        this.refreshTags();
    },
    
    methods: {
        async refreshTags() {
            this.loading = true;
            try {
                const response = await axios.get('/api/tags/');
                this.tags = response.data;
            } catch (error) {
                ElementPlus.ElMessage.error('加载标签失败');
                console.error('Failed to fetch tags:', error);
            } finally {
                this.loading = false;
            }
        },
        
        async addTag() {
            if (!this.form.name.trim()) {
                ElementPlus.ElMessage.warning('请输入标签名称');
                return;
            }
            
            this.adding = true;
            try {
                const response = await axios.post('/api/tags/', this.form);
                ElementPlus.ElMessage.success('标签添加成功');
                this.form.name = '';
                this.form.color = '#3498db';
                await this.refreshTags();
            } catch (error) {
                const msg = error.response?.data?.detail || '添加失败';
                ElementPlus.ElMessage.error(msg);
                console.error('Add tag error:', error);
            } finally {
                this.adding = false;
            }
        },
        
        async deleteTag(id) {
            try {
                await ElementPlus.ElMessageBox.confirm(
                    '确定要删除这个标签吗？删除后不可恢复。',
                    '警告',
                    {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                    }
                );
                
                this.deletingId = id;
                const response = await axios.delete(`/api/tags/${id}`);
                
                if (response.data.success) {
                    ElementPlus.ElMessage.success('删除成功');
                    await this.refreshTags();
                }
            } catch (error) {
                if (error !== 'cancel') {
                    const msg = error.response?.data?.detail || '删除失败';
                    ElementPlus.ElMessage.error(msg);
                    console.error('Delete tag error:', error);
                }
            } finally {
                this.deletingId = null;
            }
        },
        
        editTag(row) {
            this.editForm = {
                id: row.id,
                name: row.name,
                color: row.color
            };
            this.editDialogVisible = true;
        },
        
        async updateTag() {
            if (!this.editForm.name.trim()) {
                ElementPlus.ElMessage.warning('请输入标签名称');
                return;
            }
            
            this.updating = true;
            try {
                const response = await axios.put(`/api/tags/${this.editForm.id}`, this.editForm);
                ElementPlus.ElMessage.success('标签更新成功');
                this.editDialogVisible = false;
                await this.refreshTags();
            } catch (error) {
                const msg = error.response?.data?.detail || '更新失败';
                ElementPlus.ElMessage.error(msg);
                console.error('Update tag error:', error);
            } finally {
                this.updating = false;
            }
        },
        
        formatDate(dateStr) {
            if (!dateStr) return '';
            const date = new Date(dateStr);
            return date.toLocaleString('zh-CN');
        }
    }
};

// 导出组件
if (typeof window !== 'undefined') {
    window.TagManager = TagManager;
}
