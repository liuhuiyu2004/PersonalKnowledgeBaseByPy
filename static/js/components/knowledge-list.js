// 知识列表组件
// @author LiuHuiYu
const KnowledgeList = {
    template: `
        <div class="knowledge-list">
            <el-card v-if="loading" class="loading-container">
                <el-skeleton :rows="5" animated />
            </el-card>
            
            <div v-else-if="knowledgeList.length === 0" class="empty-state">
                <i>📭</i>
                <h3>暂无知识</h3>
                <p>点击上方"新建知识"添加第一条知识</p>
            </div>
            
            <el-row v-else :gutter="20">
                <el-col :xs="24" :sm="12" :md="8" v-for="item in knowledgeList" :key="item.id">
                    <el-card shadow="hover" class="knowledge-card">
                        <template #header>
                            <div class="card-header">
                                <span class="card-title">{{ item.title }}</span>
                                <el-tag size="small" :type="getSourceTypeTag(item.source_type)">{{ getSourceTypeText(item.source_type) }}</el-tag>
                            </div>
                        </template>
                        
                        <!-- 优先显示摘要，没有摘要则显示内容预览 -->
                        <div class="content-preview">
                            <div v-if="item.summary" style="color: #606266; line-height: 1.8;">
                                <i style="color: #909399;">📝</i> {{ item.summary }}
                            </div>
                            <div v-else>{{ truncateContent(item.content) }}</div>
                        </div>
                        
                        <div v-if="item.tags && item.tags.length > 0" style="margin: 10px 0;">
                            <el-tag 
                                v-for="tag in item.tags" 
                                :key="tag.id" 
                                size="small" 
                                class="tag-item"
                                :color="tag.color"
                                :effect="getTagEffect(tag.color)"
                            >
                                {{ tag.name }}
                            </el-tag>
                        </div>
                        
                        <div class="card-meta">
                            <div>创建时间：{{ formatDate(item.created_at) }}</div>
                            <div v-if="item.updated_at && item.updated_at !== item.created_at">
                                更新时间：{{ formatDate(item.updated_at) }}
                            </div>
                        </div>
                        
                        <template #footer>
                            <div class="action-buttons">
                                <el-button size="small" @click="viewDetail(item)">查看</el-button>
                                <el-button size="small" type="primary" @click="editItem(item)">编辑</el-button>
                                <el-button size="small" type="danger" @click="deleteItem(item.id)">删除</el-button>
                            </div>
                        </template>
                    </el-card>
                </el-col>
            </el-row>
            
            <!-- 分页 -->
            <el-pagination
                v-if="total > pageSize"
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next"
                :total="total"
                @size-change="fetchData"
                @current-change="fetchData"
                style="margin-top: 20px; justify-content: center; display: flex;"
            />
        </div>
    `,
    
    data() {
        return {
            knowledgeList: [],
            loading: false,
            currentPage: 1,
            pageSize: 20,
            total: 0
        }
    },
    
    created() {
        this.fetchData();
    },
    
    methods: {
        async fetchData() {
            this.loading = true;
            try {
                const skip = (this.currentPage - 1) * this.pageSize;
                const response = await axios.get('/api/knowledge/', {
                    params: {
                        skip: skip,
                        limit: this.pageSize
                    }
                });
                this.knowledgeList = response.data;
                this.total = response.data.length;
            } catch (error) {
                ElementPlus.ElMessage.error('加载失败');
                console.error('Fetch error:', error);
            } finally {
                this.loading = false;
            }
        },
        
        truncateContent(content) {
            if (!content) return '';
            return content.length > 100 ? content.substring(0, 100) + '...' : content;
        },
        
        formatDate(dateStr) {
            if (!dateStr) return '';
            const date = new Date(dateStr);
            return date.toLocaleString('zh-CN');
        },
        
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
        
        // 根据颜色深浅选择标签效果
        getTagEffect(color) {
            if (!color) return 'plain';
            
            // 将十六进制颜色转换为 RGB
            const hex = color.replace('#', '');
            const r = parseInt(hex.substr(0, 2), 16);
            const g = parseInt(hex.substr(2, 2), 16);
            const b = parseInt(hex.substr(4, 2), 16);
            
            // 计算亮度 (使用 YIQ 公式)
            const brightness = (r * 299 + g * 587 + b * 114) / 1000;
            
            // 亮色背景用 dark 效果 (白字),暗色背景用 plain 效果 (黑字)
            return brightness > 128 ? 'dark' : 'plain';
        },
        
        viewDetail(item) {
            console.log('viewDetail called with:', item);
            // 触发父组件的查看事件
            this.$emit('view', item);
        },
        
        editItem(item) {
            console.log('editItem called with:', item);
            this.$emit('edit', item);
        },
        
        async deleteItem(id) {
            // 触发父组件的删除事件
            this.$emit('delete', id);
        }
    }
};

// 导出组件
if (typeof window !== 'undefined') {
    window.KnowledgeList = KnowledgeList;
}
