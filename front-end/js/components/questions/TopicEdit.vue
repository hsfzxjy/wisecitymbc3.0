<template>
    <div class="container">
        <editor
            v-if="!$loadingRouteData"
            :model.sync="topic"
            name="topic-edit"
            base-url="/api/topics/">
            <vs-form-input
                :model.sync="topic.title"
                type="text"
                name='title'
                placeholder="标题"
                slot="fields-before">
            </vs-form-input>
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
            topic: {
                id: '',
                title: '',
                content: '', 
                attachments: []
            }
        }),
        editConfig: {
            getInitURL (id) {
                return `/api/topics/${id}/?fields=title,content,attachments`
            },
            objectFieldName: 'topic'
        }
    }
</script>