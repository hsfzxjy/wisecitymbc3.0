<template>
    <div class="rows">
        <div class="col-md-offset-2 col-md-8 col-sm-12">
            <vs-tabs size="md" :fade="false">
                <vs-tab
                    id="$key"
                    :title="category"
                    :active='$key === currentCategory'
                    v-for="category in categories">
                    <article-list
                        :category="$key">    
                    </article-list>
                </vs-tab>
            </vs-tabs>          
        </div> 
    </div>
</template>

<script>
    import _ from 'lodash'
    import ArticleList from '../lists/ArticleList.vue'
    import consts from 'consts.json'

    const AVAILABLE_CATEGORIES = ['government', 'company', 'media']
    const CATEGORIES_NAME = ['政府', '公司', '媒体']

    export default {
        components: { ArticleList },
        data: () => ({
            categories: _.zipObject(AVAILABLE_CATEGORIES, CATEGORIES_NAME)
        }),
        computed: {
            currentCategory () {
                let category = this.$route.params.category

                if (! category in AVAILABLE_CATEGORIES)
                    category = 'government'

                return category
            }
        },
        ready () {
            
        }
    }
</script>