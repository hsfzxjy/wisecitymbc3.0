<template>
    <div class="col-xs-12">
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
                label="标题"
                placeholder="标题"
                slot="fields-before">
            </vs-form-input>
            <vs-form-input
                :model.sync="tagsDisplay"
                type="text"
                name='tags'
                label='标签'
                help-text="以空格分隔"
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

<style scoped>
    div.checkbox label {
        display: block;
    }
</style>

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
                    let trimed = _.trim(value)
                    console.log(trimed, trimed.split(/\ +/))
                    this.article.tags = trimed ? trimed.split(/\ +/) : []
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