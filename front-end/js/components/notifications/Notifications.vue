<template>
    <div class="container">
        <vs-list-group flush class="col-md-8 col-sm-12">
            <vs-list-group-item
                v-for="item in page.results"
                :state="!item.has_read ? 'warning' : ''"
                @click="mark([item])">
                {{{ item.message | render }}}
            </vs-list-group-item>
        </vs-list-group>
        <pager
            :model.sync="page"
            url="/api/n/">
        </pager>
    </div>
</template>

<script>
    import Pager from 'misc/Pager.vue'

    export default {
        components: { Pager },
        filters: {
            render: message => message
                .replace(/\[(.*)\]\((.*)\)/g, (ignore, text, url) => {
                    console.log(ignore, text, url)
                    return `<a href="#!${url}">${text}</a>`
                })
        },
        data: () => ({
            page: {}
        }),
        methods: {
            mark (items) {
                this.$http.get('/api/n/mark_as_read/', {
                    params: {
                        ids: _.map(items, 'id').join(',')
                    }
                }).then(() => _.map(items, item => item.has_read = true))
            }
        }
    }
</script>