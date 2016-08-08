<template>
    <div class="rows">
        <div class="col-md-3 hidden-sm-down">
            <article-nav-bar 
                :vertical="true" 
                class="hidden-sm-down fixed"
                :current-category="currentCategory">    
            </article-nav-bar>
        </div>
        <div class="col-md-9 col-sm-12 col-md-offset-3">
            <article-list
                :category="currentCategory">    
            </article-list>         
        </div> 
    </div>
</template>

<style scoped>
</style>

<script>
    import {StrUtils} from 'utils/index.es'
    import ArticleList from './ArticleList.vue'
    import ArticleNavBar from './ArticleNavBar.vue'

    import { AVAILABLE_CATEGORIES } from 'consts.es'

    export default {
        components: { ArticleList, ArticleNavBar },
        data: () => ({
            currentCategory: ''
        }),
        route: {
            data ({to, next}) {
                let category = to.params.category

                if (!StrUtils.isContainedBy(category, AVAILABLE_CATEGORIES))
                    category = 'government'

                this.currentCategory = category
                this.$nextTick(() => { this.$broadcast('List:reload') })
            }
        }
    }
</script>