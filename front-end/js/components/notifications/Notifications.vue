<template>
    <div class="container">
        <vs-list-group flush class="col-xs-">
            <vs-list-group-item
                v-for="item in notifications"
                @click="mark([item])">
                <i class="fa fa-star text-warning" v-if="!item.has_read"></i>
                {{{ item.message | render }}}
                <span class="pull-xs-right">
                    {{ item.created_time | timesince }}
                </span>
            </vs-list-group-item>
        </vs-list-group>
        <list
            :model.sync="notifications"
            type="pager"
            url="/api/n/">
        </list>
    </div>
</template>

<script>
    export default {
        filters: {
            render: message => message
                .replace(/\[(.*)\]\((.*)\)/g, (ignore, text, url) => {
                    return `<a href="#!${url}">${text}</a>`
                })
        },
        data: () => ({
            notifications: []
        }),
        route: {
            data () {
                this.$nextTick(() => this.$broadcast('List:reload'))
            }
        },
        methods: {
            mark (items) {
                items = _.filter(items, item => !item.has_read)
                this.$http.get('/api/n/mark_as_read/', {
                    params: {
                        ids: _.map(items, 'id').join(',')
                    }
                }).then(() => {
                    this.$root.nCount -= items.length;
                    _.map(items, item => item.has_read = true)
                })
            }
        }
    }
</script>