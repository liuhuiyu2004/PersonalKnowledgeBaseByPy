// 知识图谱组件
// @author LiuHuiYu
const KnowledgeGraph = {
    template: `
        <div class="knowledge-graph">
            <el-card>
                <template #header>
                    <div class="card-header">
                        <h2>🕸️ 知识图谱</h2>
                        <div class="controls">
                            <el-button 
                                type="primary" 
                                size="small" 
                                @click="refreshData"
                                :loading="loading"
                            >
                                🔄 刷新
                            </el-button>
                            <el-button 
                                size="small" 
                                @click="toggleLayout"
                            >
                                切换布局：{{ layout === 'force' ? '力导向' : '环形' }}
                            </el-button>
                        </div>
                    </div>
                </template>
                
                <div v-loading="loading" element-loading-text="加载中...">
                    <div ref="chartContainer" class="chart-container"></div>
                    
                    <div v-if="!loading && nodes.length === 0" class="empty-state">
                        <i>📭</i>
                        <h3>暂无数据</h3>
                        <p>请先添加一些知识和标签</p>
                    </div>
                </div>
                
                <div class="legend">
                    <h4>图例说明:</h4>
                    <div class="legend-items">
                        <div class="legend-item">
                            <span class="legend-icon knowledge-icon">📄</span>
                            <span>知识条目</span>
                        </div>
                        <div class="legend-item">
                            <span class="legend-icon tag-icon">🏷️</span>
                            <span>标签</span>
                        </div>
                        <div class="legend-item">
                            <span class="legend-line"></span>
                            <span>关联关系</span>
                        </div>
                    </div>
                </div>
            </el-card>
        </div>
    `,
    
    data() {
        return {
            chart: null,
            nodes: [],
            links: [],
            loading: false,
            layout: 'force' // 'force' 或 'circular'
        }
    },
    
    mounted() {
        this.initChart();
        this.fetchData();
        window.addEventListener('resize', this.handleResize);
    },
    
    beforeUnmount() {
        if (this.chart) {
            this.chart.dispose();
        }
        window.removeEventListener('resize', this.handleResize);
    },
    
    methods: {
        initChart() {
            if (!this.$refs.chartContainer) return;
            
            this.chart = echarts.init(this.$refs.chartContainer);
            
            // 点击事件
            this.chart.on('click', (params) => {
                if (params.dataType === 'node') {
                    this.handleNodeClick(params.data);
                }
            });
        },
        
        async fetchData() {
            this.loading = true;
            try {
                const [knowledgeRes, tagsRes] = await Promise.all([
                    axios.get('/api/knowledge/', { params: { limit: 100 } }),
                    axios.get('/api/tags/')
                ]);
                
                const knowledgeList = knowledgeRes.data;
                const tagList = tagsRes.data;
                
                // 构建节点和边
                this.buildGraphData(knowledgeList, tagList);
                
                // 更新图表
                this.updateChart();
            } catch (error) {
                ElementPlus.ElMessage.error('加载图谱数据失败');
                console.error('Fetch graph data error:', error);
            } finally {
                this.loading = false;
            }
        },
        
        buildGraphData(knowledgeList, tagList) {
            const nodes = [];
            const links = [];
            
            // 添加知识节点
            knowledgeList.forEach(k => {
                nodes.push({
                    id: `knowledge_${k.id}`,
                    name: k.title,
                    symbolSize: 40,
                    value: k.title,
                    category: 0, // 知识类别
                    draggable: true,
                    knowledgeId: k.id,
                    sourceType: k.source_type,
                    tags: k.tags || []
                });
                
                // 添加知识与标签的连线
                if (k.tags && k.tags.length > 0) {
                    k.tags.forEach(tag => {
                        links.push({
                            source: `knowledge_${k.id}`,
                            target: `tag_${tag.id}`,
                            label: { show: false }
                        });
                    });
                }
            });
            
            // 添加标签节点
            tagList.forEach(tag => {
                // 只添加有知识关联的标签
                const hasKnowledge = knowledgeList.some(k => 
                    k.tags && k.tags.some(t => t.id === tag.id)
                );
                
                if (hasKnowledge) {
                    nodes.push({
                        id: `tag_${tag.id}`,
                        name: tag.name,
                        symbolSize: 30,
                        value: tag.name,
                        category: 1, // 标签类别
                        draggable: true,
                        tagId: tag.id,
                        color: tag.color
                    });
                }
            });
            
            this.nodes = nodes;
            this.links = links;
        },
        
        updateChart() {
            if (!this.chart) return;
            
            const option = {
                tooltip: {
                    trigger: 'item',
                    formatter: (params) => {
                        if (params.dataType === 'node') {
                            const data = params.data;
                            if (data.category === 0) {
                                // 知识节点
                                return `
                                    <strong>📄 ${data.name}</strong><br/>
                                    类型：${this.getSourceTypeText(data.sourceType)}<br/>
                                    标签数：${data.tags ? data.tags.length : 0}
                                `;
                            } else {
                                // 标签节点
                                return `<strong>🏷️ ${data.name}</strong>`;
                            }
                        }
                        return params.name;
                    }
                },
                legend: [{
                    data: ['知识', '标签'],
                    bottom: 10,
                    left: 'center'
                }],
                series: [
                    {
                        type: 'graph',
                        layout: this.layout,
                        data: this.nodes,
                        links: this.links,
                        roam: true,
                        label: {
                            show: true,
                            position: 'right',
                            formatter: '{b}',
                            fontSize: 12
                        },
                        lineStyle: {
                            color: 'source',
                            curveness: 0.3,
                            width: 1.5
                        },
                        emphasis: {
                            focus: 'adjacency',
                            lineStyle: {
                                width: 3
                            }
                        },
                        categories: [
                            {
                                name: '知识',
                                itemStyle: {
                                    color: '#409EFF'
                                }
                            },
                            {
                                name: '标签',
                                itemStyle: {
                                    color: '#67C23A'
                                }
                            }
                        ]
                    }
                ]
            };
            
            this.chart.setOption(option, true);
        },
        
        handleNodeClick(data) {
            if (data.category === 0) {
                // 点击知识节点，查看详情
                this.viewKnowledge(data.knowledgeId);
            } else if (data.category === 1) {
                // 点击标签节点，筛选该标签的知识
                this.filterByTag(data.tagId);
            }
        },
        
        viewKnowledge(id) {
            // 触发父组件的查看事件
            this.$emit('view-knowledge', id);
        },
        
        filterByTag(tagId) {
            // 触发父组件的筛选事件
            this.$emit('filter-by-tag', tagId);
        },
        
        refreshData() {
            this.fetchData();
        },
        
        toggleLayout() {
            this.layout = this.layout === 'force' ? 'circular' : 'force';
            this.updateChart();
        },
        
        handleResize() {
            if (this.chart) {
                this.chart.resize();
            }
        },
        
        getSourceTypeText(type) {
            const texts = {
                'manual': '手动',
                'web': '网页',
                'api': 'API'
            };
            return texts[type] || type;
        }
    }
};
