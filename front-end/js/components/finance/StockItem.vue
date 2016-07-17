<template>
    <div>
        <vs-card>
            <div class="card-block text-xs-center">
                <h3>
                    {{ stock.name }}
                </h3>
                <dl class="clearfix">
                    <dt class="col-md-6">价格</dt>
                    <dd class="col-md-6">{{ stock.price }}</dd>
                    <dt class="col-md-6">成交量</dt>
                    <dd class="col-md-6">{{ stock.volume }}</dd>
                </dl>
            </div>
            <vs-list-group flush v-if="detail">
                <vs-list-group-item>
                    <vs-expansion
                        title="公司简介">
                        <div slot="content">
                            {{{ stock.company_info | br }}}
                        </div>
                    </vs-expansion>
                </vs-list-group-item>
                <vs-list-group-item>
                    <vs-expansion
                        title="券商评价">
                        <div slot="content">
                            <vs-list-group flush>
                                <vs-list-group-item
                                    v-for="comment in stock.comments">
                                    {{{ comment.content | br }}}
                                </vs-list-group-item>
                            </vs-list-group>
                        </div>
                    </vs-expansion>
                </vs-list-group-item>
                <vs-list-group-item
                    class="no-padding">
                    <chart
                        :url="'/api/stocks/'+stock.id+'/logs/?limit=5'"
                        :series.once="chartSeries">
                            
                    </chart>
                </vs-list-group-item>
            </vs-list-group>
        </vs-card>
    </div>
</template>

<style scoped>
    .card hr {
        margin: 0;
    }
</style>

<script>
    import Chart from 'misc/Chart.vue'

    export default {
        components: { Chart },
        data: () => ({
            chartSeries: {
                price: {
                    name: '价格'
                },
                volume: {
                    name: '成交量'
                }
            }
        }),
        props: {
            stock: {
                type: Object,
                required: true
            },
            detail: {
                type: Boolean,
                default: true
            }
        }
    }
</script>