<template>
    <div class="container">
        <editor
            v-if="!$loadingRouteData"
            name="article-edit"
            base-url="/api/articles/"
            :model.sync="article">
            <vs-form-input
                :model.sync="article.title"
                type="text"
                name='title'
                placeholder="标题"
                slot="fields-before">
            </vs-form-input>
        </editor>
    </div>
</template>

<script>
    import _ from 'lodash'
    import Editor from 'components/edit/Editor.vue'
    import EditPageMixin from 'components/mixins/EditPageMixin.es'

    export default {
        mixins: [EditPageMixin],
        components: { Editor },
        data: () => ({
            article: {
                id: '',
                title: '',
                content: '', 
                attachments: []
            }
        }),
        editConfig: {
            getInitURL (id) {
                return `/api/articles/${id}/?fields=title,content,attachments`
            },
            objectFieldName: 'article'
        }
    }
</script>