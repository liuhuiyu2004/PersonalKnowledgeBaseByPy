// 应用主入口
// @author LiuHuiYu

// API 基础 URL
const API_BASE = window.location.origin;

// axios 配置
axios.defaults.baseURL = API_BASE;
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Vue 应用实例
const { createApp, h } = Vue;

const app = createApp({
    data() {
        return {
            currentView: 'list',
            editData: null,
        }
    },
    watch: {
        editData: {
            handler(newVal) {
                console.log('editData changed:', newVal);
                console.log('editData.content:', newVal ? newVal.content : 'null');
                console.log('editData.content length:', newVal && newVal.content ? newVal.content.length : 0);
            },
            deep: true
        }
    },
    components: {
        // 注册全局组件
        'knowledge-list': KnowledgeList,
        'knowledge-editor': KnowledgeEditor,
        'search-view': SearchView,
        'web-crawler': WebCrawler,
        'tag-manager': TagManager,
        'knowledge-graph': KnowledgeGraph,
        'statistics': Statistics
    },
    methods: {
        // 编辑知识
        async editKnowledge(knowledge) {
            console.log('Edit knowledge:', knowledge);
            console.log('Knowledge tags:', knowledge.tags);
            
            // 通过 ID 获取完整的知识详情
            try {
                const response = await axios.get(`/api/knowledge/${knowledge.id}`);
                console.log('Full knowledge data:', response.data);
                this.editData = response.data;
                this.currentView = 'create';
            } catch (error) {
                console.error('Load knowledge for edit error:', error);
                ElementPlus.ElMessage.error('加载知识详情失败');
            }
        },
        
        // 删除知识
        async deleteKnowledge(id) {
            try {
                await ElementPlus.ElMessageBox.confirm(
                    '确定要删除这条知识吗？',
                    '警告',
                    {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                    }
                );
                        
                const response = await axios.delete(`/api/knowledge/${id}`);
                console.log('Delete response:', response.data);
                        
                if (response.data.success) {
                    ElementPlus.ElMessage.success('删除成功');
                    // 直接刷新列表组件
                    this.$nextTick(() => {
                        if (this.$refs.knowledgeList) {
                            console.log('Refreshing knowledge list...');
                            this.$refs.knowledgeList.fetchData();
                        } else {
                            console.log('knowledgeList ref not found');
                        }
                    });
                } else {
                    ElementPlus.ElMessage.error('删除失败');
                }
            } catch (error) {
                if (error !== 'cancel') {
                    ElementPlus.ElMessage.error('删除失败:' + (error.response?.data?.detail || error.message));
                    console.error('Delete error:', error);
                }
            }
        },
        
        // 查看知识
        viewKnowledge(knowledge) {
            console.log('Viewing knowledge:', knowledge);
                    
            const { h } = Vue;
                    
            // 创建内容区域 - 使用 innerHTML 渲染富文本
            const contentVNode = h('div', {
                style: {
                    'line-height': '1.8',
                    'max-height': '60vh',
                    'overflow-y': 'auto',
                    'margin-top': '15px'
                },
                innerHTML: knowledge.content
            });
                    
            // 创建头部信息（标签和日期）
            const headerVNode = h('div', {
                style: {
                    'margin-bottom': '15px',
                    'padding-bottom': '10px',
                    'border-bottom': '1px solid #e4e7ed'
                }
            }, [
                h('el-tag', {
                    type: this.getSourceTypeTag(knowledge.source_type),
                    size: 'small'
                }, this.getSourceTypeText(knowledge.source_type)),
                h('span', {
                    style: {
                        'margin-left': '10px',
                        'color': '#909399',
                        'font-size': '13px'
                    }
                }, this.formatDate(knowledge.created_at))
            ]);
                    
            // 使用 ElementPlus 的 Dialog 组件
            ElementPlus.ElMessageBox.alert(
                h('div', [headerVNode, contentVNode]),
                knowledge.title,
                {
                    dangerouslyUseHTMLString: true,  // 启用 HTML 渲染
                    confirmButtonText: '关闭',
                    width: '80%',
                    customStyle: {
                        maxWidth: '1200px'
                    }
                }
            );
        },
                
        // 通过 ID 查看知识
        async viewKnowledgeById(id) {
            try {
                const response = await axios.get(`/api/knowledge/${id}`);
                this.viewKnowledge(response.data);
            } catch (error) {
                ElementPlus.ElMessage.error('加载知识详情失败');
                console.error('Load knowledge error:', error);
            }
        },
                
        // 按标签筛选
        filterByTag(tagId) {
            console.log('Filter by tag:', tagId);
            // 切换到搜索页面
            this.currentView = 'search';
            // 等待搜索页面加载后，设置筛选条件
            this.$nextTick(() => {
                if (this.$refs.searchView) {
                    console.log('Calling searchView.filterByTag with tagId:', tagId);
                    this.$refs.searchView.filterByTag(tagId);
                } else {
                    console.error('searchView ref not found');
                }
            });
        },
        
        // 辅助方法
        getSourceTypeTag(type) {
            const types = {
                'manual': '',
                'web': 'success',
                'api': 'warning'
            };
            return types[type] || '';
        },
        
        getSourceTypeText(type) {
            const texts = {
                'manual': '手动',
                'web': '网页',
                'api': 'API'
            };
            return texts[type] || type;
        },
        
        formatDate(dateStr) {
            if (!dateStr) return '';
            const date = new Date(dateStr);
            return date.toLocaleString('zh-CN');
        },
        
        // 保存成功
        saveSuccess() {
            ElementPlus.ElMessage.success('保存成功');
            this.currentView = 'list';
            this.editData = null;
        },
        
        // 取消编辑
        cancelEdit() {
            this.editData = null;
            this.currentView = 'list';
        }
    }
});

// 使用 Element Plus
app.use(ElementPlus);

// 挂载应用
app.mount('#app');
