<template>
    <div>
        <vs-card>
            <div class="card-block text-xs-center">
                <h3>
                    {{ future.name }}
                </h3>
                <dl class="clearfix">
                    <dt class="col-md-6">价格</dt>
                    <dd class="col-md-6">{{ future.price }}</dd>
                </dl>
            </div>
            <vs-list-group flush>
                <vs-list-group-item
                    class="no-padding">
                    <chart
                        :url="`/api/futures/${future.id}/logs/?limit=5`"
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
                }
            }
        }),
        props: {
            future: {
                type: Object,
                required: true
            }
        }
    }
</script>