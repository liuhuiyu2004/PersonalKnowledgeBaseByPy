// 搜索视图组件
// @author LiuHuiYu
const SearchView = {
    template: `
        <div class="search-view">
            <el-card>
                <h2>🔍 搜索知识</h2>
                
                <el-input
                    v-model="searchQuery"
                    placeholder="输入关键词搜索..."
                    size="large"
                    clearable
                    @keyup.enter="search"
                    class="search-box"
                >
                    <template #prefix>
                        <el-icon><Search /></el-icon>
                    </template>
                    <template #append>
                        <el-button @click="search">搜索</el-button>
                    </template>
                </el-input>
                
                <!-- 高级筛选 -->
                <el-collapse style="margin-bottom: 20px;">
                    <el-collapse-item title="高级筛选" name="1">
                        <el-form :inline="true">
                            <el-form-item label="标签">
                                <el-select v-model="filterTagIds" multiple placeholder="选择标签" style="width: 200px;">
                                    <el-option
                                        v-for="tag in allTags"
                                        :key="tag.id"
                                        :label="tag.name"
                                        :value="tag.id"
                                    />
                                </el-select>
                            </el-form-item>
                            <el-form-item label="来源">
                                <el-select v-model="filterSourceType" placeholder="全部" clearable style="width: 150px;">
                                    <el-option label="手动" value="manual" />
                                    <el-option label="网页" value="web" />
                                    <el-option label="API" value="api" />
                                </el-select>
                            </el-form-item>
                        </el-form>
                    </el-collapse-item>
                </el-collapse>
            </el-card>
            
            <!-- 搜索结果 -->
            <div v-if="searchResults.length > 0" style="margin-top: 20px;">
                <el-card v-for="item in searchResults" :key="item.id" shadow="hover" class="knowledge-card">
                    <template #header>
                        <div class="card-header">
                            <span class="card-title">{{ item.title }}</span>
                            <el-tag size="small" :type="getSourceTypeTag(item.source_type)">
                                {{ getSourceTypeText(item.source_type) }}
                            </el-tag>
                        </div>
                    </template>
                    
                    <div class="content-preview">{{ highlightText(truncateContent(item.content)) }}</div>
                    
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
                        创建时间：{{ formatDate(item.created_at) }}
                    </div>
                    
                    <template #footer>
                        <div class="action-buttons">
                            <el-button size="small" @click="viewDetail(item)">查看</el-button>
                            <el-button size="small" type="primary" @click="editItem(item)">编辑</el-button>
                        </div>
                    </template>
                </el-card>
                
                <el-pagination
                    v-if="total > pageSize"
                    v-model:current-page="currentPage"
                    v-model:page-size="pageSize"
                    :page-sizes="[10, 20, 50]"
                    layout="total, sizes, prev, pager, next"
                    :total="total"
                    @size-change="search"
                    @current-change="search"
                    style="margin-top: 20px; justify-content: center; display: flex;"
                />
            </div>
            
            <!-- 空状态 -->
            <div v-else-if="searched" class="empty-state">
                <i>🔎</i>
                <h3>未找到相关结果</h3>
                <p>试试其他关键词或调整筛选条件</p>
            </div>
        </div>
    `,
    
    data() {
        return {
            searchQuery: '',
            searchResults: [],
            searched: false,
            currentPage: 1,
            pageSize: 20,
            total: 0,
            allTags: [],
            filterTagIds: [],
            filterSourceType: ''
        }
    },
    
    created() {
        this.fetchTags();
    },
    
    methods: {
        async fetchTags() {
            try {
                const response = await axios.get('/api/tags/');
                this.allTags = response.data;
            } catch (error) {
                console.error('Failed to fetch tags:', error);
            }
        },
        
        async search() {
            // 如果没有搜索词但有标签筛选，也可以执行搜索
            if (!this.searchQuery.trim() && this.filterTagIds.length === 0 && !this.filterSourceType) {
                ElementPlus.ElMessage.warning('请输入搜索关键词');
                return;
            }
            
            console.log('Executing search with:', {
                query: this.searchQuery,
                tag_ids: this.filterTagIds,
                source_type: this.filterSourceType
            });
            
            const skip = (this.currentPage - 1) * this.pageSize;
            
            try {
                const response = await axios.post('/api/search/', {
                    query: this.searchQuery,
                    page: this.currentPage,
                    page_size: this.pageSize,
                    tag_ids: this.filterTagIds.length > 0 ? this.filterTagIds : null,
                    source_type: this.filterSourceType || null
                });
                
                console.log('Search response:', response.data);
                
                this.searchResults = response.data.results;
                this.total = response.data.total;
                this.searched = true;
                
                if (this.total === 0) {
                    ElementPlus.ElMessage.info('未找到相关结果');
                } else {
                    ElementPlus.ElMessage.success(`找到 ${this.total} 条结果`);
                }
            } catch (error) {
                ElementPlus.ElMessage.error('搜索失败');
                console.error('Search error:', error);
            }
        },
        
        truncateContent(content) {
            if (!content) return '';
            return content.length > 150 ? content.substring(0, 150) + '...' : content;
        },
        
        highlightText(text) {
            if (!this.searchQuery) return text;
            const regex = new RegExp(`(${this.searchQuery})`, 'gi');
            return text.replace(regex, '<mark>$1</mark>');
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
            this.$emit('view', item);
        },
        
        editItem(item) {
            this.$emit('edit', item);
        },
        
        // 按标签筛选（供外部调用）
        filterByTag(tagId) {
            console.log('SearchView.filterByTag called with tagId:', tagId);
            // 设置筛选标签
            this.filterTagIds = [tagId];
            // 清空搜索词，执行筛选
            this.searchQuery = '';
            this.currentPage = 1;
            
            // 直接调用搜索方法
            this.search();
        }
    }
};

// 导出组件
if (typeof window !== 'undefined') {
    window.SearchView = SearchView;
}
