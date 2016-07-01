<template>
    <div class="rows">
        <div class="col-md-offset-1 col-md-10 col-sm-12">
            <vs-nav 
                type="pills">
                <vs-nav-item
                    v-for="category in categories"
                    :link="`/articles/${$key}/`"
                    :active='$key === currentCategory'>
                    {{ category }}
                </vs-nav-item>
            </vs-nav>
            <article-list
                :category="currentCategory">    
            </article-list>         
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
            categories: _.zipObject(AVAILABLE_CATEGORIES, CATEGORIES_NAME),
            currentCategory: ''
        }),
        route: {
            data (transition) {
                let category = transition.to.params.category

                if (! (_.indexOf(AVAILABLE_CATEGORIES, category) >= 0))
                    category = 'government'

                this.currentCategory = category
            }
        },
        ready () {
            
        }
    }
</script>