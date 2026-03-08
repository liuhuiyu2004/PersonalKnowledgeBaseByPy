// 统计组件
// @author LiuHuiYu
const Statistics = {
    template: `
        <div class="statistics">
            <h2>📊 统计信息</h2>
            
            <!-- 总体统计 -->
            <el-row :gutter="20" style="margin-top: 20px;">
                <el-col :xs="24" :sm="12" :md="6">
                    <el-card shadow="hover" class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                        <div class="stat-label">知识总数</div>
                        <div class="stat-number">{{ stats.total_knowledge || 0 }}</div>
                    </el-card>
                </el-col>
                
                <el-col :xs="24" :sm="12" :md="6">
                    <el-card shadow="hover" class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                        <div class="stat-label">标签数量</div>
                        <div class="stat-number">{{ stats.total_tags || 0 }}</div>
                    </el-card>
                </el-col>
                
                <el-col :xs="24" :sm="12" :md="6">
                    <el-card shadow="hover" class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                        <div class="stat-label">来源记录</div>
                        <div class="stat-number">{{ stats.total_sources || 0 }}</div>
                    </el-card>
                </el-col>
                
                <el-col :xs="24" :sm="12" :md="6">
                    <el-card shadow="hover" class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                        <div class="stat-label">最近 7 天新增</div>
                        <div class="stat-number">{{ stats.recent_count || 0 }}</div>
                    </el-card>
                </el-col>
            </el-row>
            
            <!-- 热门标签 -->
            <el-card style="margin-top: 20px;">
                <template #header>
                    <div class="card-header">
                        <span>🏷️ 热门标签</span>
                    </div>
                </template>
                
                <div v-if="popularTags.length > 0">
                    <el-tag
                        v-for="tag in popularTags"
                        :key="tag.id"
                        :color="tag.color"
                        effect="plain"
                        size="large"
                        style="margin: 5px;"
                    >
                        {{ tag.name }} ({{ tag.count }})
                    </el-tag>
                </div>
                <div v-else class="empty-state">
                    <p>暂无标签数据</p>
                </div>
            </el-card>
            
            <!-- 最近知识 -->
            <el-card style="margin-top: 20px;">
                <template #header>
                    <div class="card-header">
                        <span>📝 最近添加的知识</span>
                        <el-button size="small" @click="loadRecent">刷新</el-button>
                    </div>
                </template>
                
                <el-table :data="recentKnowledge" stripe style="width: 100%">
                    <el-table-column prop="title" label="标题" show-overflow-tooltip />
                    <el-table-column prop="source_type" label="来源" width="100">
                        <template #default="scope">
                            <el-tag size="small" :type="getSourceTypeTag(scope.row.source_type)">
                                {{ getSourceTypeText(scope.row.source_type) }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="created_at" label="创建时间" width="180">
                        <template #default="scope">
                            {{ formatDate(scope.row.created_at) }}
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="150">
                        <template #default="scope">
                            <el-button size="small" @click="viewDetail(scope.row)">查看</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-card>
        </div>
    `,
    
    data() {
        return {
            stats: {},
            popularTags: [],
            recentKnowledge: []
        }
    },
    
    created() {
        this.loadStats();
        this.loadPopularTags();
        this.loadRecent();
    },
    
    methods: {
        async loadStats() {
            try {
                const response = await axios.get('/api/stats/');
                this.stats = response.data;
            } catch (error) {
                console.error('Failed to load stats:', error);
            }
        },
        
        async loadPopularTags() {
            try {
                const response = await axios.get('/api/stats/popular/tags');
                this.popularTags = response.data;
            } catch (error) {
                console.error('Failed to load popular tags:', error);
            }
        },
        
        async loadRecent() {
            try {
                const response = await axios.get('/api/stats/recent?limit=10');
                this.recentKnowledge = response.data;
            } catch (error) {
                console.error('Failed to load recent knowledge:', error);
            }
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
        
        viewDetail(item) {
            ElementPlus.ElDialog({
                title: item.title,
                width: '80%',
                content: () => h('div', [
                    h('div', { style: 'margin-bottom: 20px;' }, [
                        h('el-tag', { type: this.getSourceTypeTag(item.source_type) }, this.getSourceTypeText(item.source_type)),
                        h('span', { style: 'margin-left: 10px; color: #909399;' }, this.formatDate(item.created_at))
                    ]),
                    h('div', { style: 'white-space: pre-wrap; line-height: 1.8;' }, item.content)
                ]),
                showConfirmButton: false,
                closeOnPressEscape: true,
            });
        }
    }
};

// 导出组件
if (typeof window !== 'undefined') {
    window.Statistics = Statistics;
}
