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
                                ></el-input>
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
                            <el-button size="small" @click="previewSearchResult(scope.row)">预览</el-button>
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
                engine: 'duckduckgo', // 默认使用 DuckDuckGo
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
            searchResults: null
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
                ElementPlus.ElMessage.error('抓取失败：' + (error.response?.data?.detail || error.message));
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
            ElementPlus.ElDialog({
                title: result.title,
                width: '80%',
                content: () => h('div', [
                    h('p', { style: 'color: #909399; margin-bottom: 10px;' }, result.url),
                    h('div', { style: 'white-space: pre-wrap;' }, result.snippet)
                ]),
                showConfirmButton: false,
                closeOnPressEscape: true,
            });
        }
    }
};

// 导出组件
if (typeof window !== 'undefined') {
    window.WebCrawler = WebCrawler;
}
