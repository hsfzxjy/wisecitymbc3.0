<template>
    <span 
        @click="toggleClicked"
        :target="id">
        <slot name="title">
            <a href="javascript:void 0" style="display: block;">{{ title }}</a>
        </slot>
    </span>
    <vs-collapse
        :id="id">
        <slot name="content"></slot>
    </vs-collapse>
</template>

<script>
    import { StrUtils } from 'utils/index.es'

    export default {
        computed: {
            id () {
                return StrUtils.randStr()
            }
        },
        props: {
            title: {
                type: String,
                default: ''
            }
        },
        methods: {
            toggleClicked () {
                jQuery('#'+this.id).slideToggle()
            }
        }
    }
</script>