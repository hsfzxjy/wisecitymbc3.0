<template>
    <div class="container">
        <h2>{{ topic.title }}</h2>
        <p>
            {{ topic.content }}
        </p>
        <reply-list
            :replies.sync="replies"
            :topic-id="topicId"
            v-if="!$loadingRouteData">
        </reply-list>
        <editor
            :model.sync="reply"
            name="topic-reply-edit"
            :base-url="`/api/topics/${topicId}/replies/`"
            @submitted="editorSubmitted"
        >
        </editor>
    </div>
</template>

<script>
    import _ from 'lodash'
    import Editor from 'components/edit/Editor.vue'
    import DetailMixin from 'components/mixins/DetailMixin.es'
    import ReplyList from 'components/lists/ReplyList.vue'

    export default {
        mixins: [DetailMixin],
        components: {ReplyList, Editor},
        detailConfig: {
            baseURL: '/api/topics/',
            objectFieldName: 'topic',
            idFieldName: 'topicId'
        },
        data: () => ({
            topic: {},
            topicId: '',
            replies: [],
            reply: {
                content: '',
                attachments: []
            }
        }),
        methods: {
            editorSubmitted (editor, reply) {
                this.replies.push(reply)
            }
        }
    }
</script>