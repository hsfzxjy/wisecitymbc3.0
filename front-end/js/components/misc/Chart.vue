<template>
    <div>
        <div :id="containerId"></div>
        <vs-buttons 
            block 
            size="sm" 
            variant="info-outline"
            @click="loadData"
            :disabled="!url || (loading || !initiated)">
            加载更多
        </vs-buttons>
    </div>
</template>

<script>
    import Highcharts from 'highcharts/highstock'

    export default {
        data: () => ({
            loading: false,
            initiated: false
        }),
        props: {
            series: {
                type: Object,
                required: true,
                coerce (val) {
                    let counter = 0

                    _.forEach(val, item => item.index = counter++)

                    return val
                }
            },
            url: {
                type: String,
                required: true
            },
            autoInit: {
                type: Boolean,
                default: true
            }
        },
        computed: {
            containerId () {
                return `chart-${Date.now()}`
            }
        },
        events: {
            ['Chart:init'] () {
                if (!this.initiated) this.init()
            }
        },
        methods: {
            initChart () {
                let series = []
                _.forEach(this.series, item => series[item.index] = {
                    name: item.name
                })

                this.chart = Highcharts.StockChart(this.containerId, {
                    chart: {
                        backgroundColor: null
                    },
                    rangeSelector: {
                        enabled: false
                    },
                    plotOptions: {
                        series: {
                            compare: 'percent'
                        }
                    },
                    tooltip: {
                        valueDecimals: 2
                    },
                    xAxis: {
                        labels: {
                            style: {
                                color: '#eee'
                            }
                        }
                    },
                    yAxis: {
                        labels: {
                            formatter: function () {
                                return (this.value > 0 ? '+' : '') + this.value + '%';
                            },
                            style: {
                                color: '#eee'
                            }
                        },
                        plotLines: [{
                            value: 0,
                            width: 2,
                            color: 'silver'
                        }],
                    },
                    series: series
                })
            },
            loadData () {
                if (!this.url || !this.initiated) return

                this.$http.get(this.url)
                    .then(({ data }) => {
                        this.addData(data.results)
                        this.url = data.next
                    })
            },
            addData (data) {
                _.forEach(this.series, ({ index }, fieldName) => {
                    let series = this.chart.series[index]

                    _.forEach(data, item => {
                        series.addPoint([+(new Date(item.created_time)), item[fieldName]])
                    })
                })
            },
            init () {
                this.initChart()
                this.initiated = true
                this.loadData()
            }
        },
        ready () {
            if (this.autoInit) this.init()
        }
    }
</script>