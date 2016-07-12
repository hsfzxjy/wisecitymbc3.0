<template>
    <div class="container">
        <div>
            <vs-badge
                v-for="tag in tags"
                :variant="tag.id == currentTagId ? 'danger' : 'info' "
                >
                <a v-link="'/tags/'+tag.id+'/'">{{tag.name}}</a>
            </vs-badge>
        </div>
        <article-list
            :other-params="{ tags__id: currentTagId }">
        </article-list>
    </div>
</template>

<style scoped>
    .label {
        margin: 0.2rem 0.4rem;
    }
    .label a {
        color: #fff;
    }
</style>

<script>
    import ArticleList from './ArticleList.vue'

    export default {
        components: { ArticleList },
        data: () => ({
            tags: [],
            currentTagId: 0
        }),
        methods: {
            loadTags () {
                return this.$http.get('/api/tags/', { params: { limit: -1}})
            }
        },
        route: {
            data (transition) {
                let id = transition.to.params.id || 0

                if (_.startsWith(transition.from.path, '/tags')) 
                    transition.next({ currentTagId: id})
                else
                    return this.loadTags()
                        .then(res => ({
                            tags: res.data.results,
                            currentTagId: id
                        }))
            }
        },
        watch: {
            currentTagId () {
                this.$broadcast('ArticleList:reset')
            }
        }
    }
</script>