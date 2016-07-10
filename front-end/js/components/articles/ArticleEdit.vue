<template>
    <div class="container">
        <editor
            v-if="!$loadingRouteData"
            name="article-edit"
            base-url="/api/articles/"
            :model.sync="article"
            @submitted="submitted">
            <vs-form-input
                :model.sync="article.title"
                type="text"
                name='title'
                placeholder="标题"
                slot="fields-before">
            </vs-form-input>
            <vs-form-input
                :model.sync="tagsDisplay"
                type="text"
                name='tags'
                placeholder="标签"
                slot="fields-before">
            </vs-form-input>
            <fieldset class="form-group" slot="fields-after">
                <div class="checkbox">
                    <label>
                        <input type="checkbox" v-model="article.is_top">
                        置顶
                    </label>
                </div>
            </fieldset>
        </editor>
    </div>
</template>

<script>
    import Editor from 'misc/edit/Editor.vue'
    import EditPageMixin from 'mixins/EditPageMixin.es'

    export default {
        mixins: [EditPageMixin],
        components: { Editor },
        data: () => ({
            article: {
                id: '',
                title: '',
                content: '', 
                tags: [],
                attachments: [],
                is_top: false
            }
        }),
        editConfig: {
            getInitURL (id) {
                return `/api/articles/${id}/?fields=title,content,attachments,tags,is_top,id`
            },
            objectFieldName: 'article'
        },
        computed: {
            tagsDisplay: {
                get () {
                    return this.article.tags.join(' ')
                },
                set (value) {
                    this.article.tags = _.trim(value).split(/\ +/)
                }
            }
        },
        methods: {
            submitted (editor, article) {
                this.$router.go(article.url)
            }
        }
    }
</script>