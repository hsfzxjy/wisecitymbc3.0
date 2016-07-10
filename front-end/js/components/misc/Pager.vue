<template>
    <div>
        <vs-pager v-if="model">
            <li v-show="model.previous" :class="!loading || 'disabled'">
                <a @click.stop="load(model.previous)" href="javascript:void(0);">Previous</a>
            </li>
            <li v-show="model.next" :class="!loading || 'disabled'">
                <a @click.stop="load(model.next)" href="javascript:void(0);">Next</a>
            </li>
        </vs-pager>        
    </div>
</template>

<script>
    export default {
        data: () => ({
            loading: false
        }),
        props: {
            model: {
                type: Object,
                twoWay: true,
                required: true
            },
            url: {
                type: String,
                required: true
            }
        },
        ready () {
            this.refresh()
        },
        methods: {
            load (url) {
                this.$http.get(url)
                    .then(res => this.model = res.data)
            },
            refresh () {
                this.load(this.url)
            }
        },
        events: {
            ['Pager:refresh'] () {
                this.refresh()
            }
        }
    }
</script>