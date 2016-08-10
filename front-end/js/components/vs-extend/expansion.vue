<template>
    <span 
        @click="toggleClicked"
        :target="id"
        v-if="!togglerId">
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
    import { randStr } from 'utils'

    export default {
        computed: {
            id () {
                return randStr()
            }
        },
        ready () {
            if (this.togglerId) 
                jQuery('#' + this.togglerId).click(() => {
                    this.toggleClicked()
                })
        },
        props: {
            togglerId: {
                type: String,
                default: ''
            },
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