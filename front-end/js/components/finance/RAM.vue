<template>
    <div class="clearfix">
        <div class="col-xs-12 col-sm-6 col-md-8">
            <h3 style="color:#ccc">原材料</h3>
            <ram-item
                v-if="items"
                v-for="item in items"
                :model="item">
            </ram-item>
            <list
                :model.sync="items"
                url="/api/raw_materials/"
                type="pager">
            </list>
        </div>
        <div class="col-xs-12 col-sm-6 col-md-4">
            <h3 style='color:#ccc'>
                资讯
            </h3>
            <article-list-group
                category="energy_and_raw_materials"
                :other-params="{ limit: 10, fields: 'id,url,title,is_top,summary' }"
                :flush="true">
            </article-list-group>
        </div>
    </div>
</template>

<style scoped>
    h3 {
        margin-bottom: 0.8rem;
    }
</style>

<script>
    import ArticleListGroup from 'articles/ArticleListGroup.vue'
    import RAMItem from './RAMItem.vue'

    export default {
        components: { ArticleListGroup, RAMItem },
        data: () => ({
            items: []
        }),
        route: {
            data (transition) {
                this.$broadcast('List:reload')
            }
        }
    }
</script>