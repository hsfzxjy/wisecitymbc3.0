<template>
    <div :class="class">
        <vs-nav 
            type="pills" :vertical="vertical">
            <vs-nav-item
                v-for="category in categories"
                :link="`/articles/${$key}/`"
                :active='$key === currentCategory'>
                {{ category }}
            </vs-nav-item>
        </vs-nav>
    </div>
</template>

<script>
    import _ from 'lodash'
    import { AVAILABLE_CATEGORIES } from 'components/consts.es'
    const CATEGORIES_NAME = ['政府', '公司', '媒体']

    export default {
        data: () => ({
            categories: _.zipObject(AVAILABLE_CATEGORIES, CATEGORIES_NAME),
        }),
        props: {
            vertical: {
                type: Boolean,
                default: false
            },
            class: {
                default: ''
            },
            currentCategory: {
                type: String,
                default: 'none'
            }
        },
    }
</script>