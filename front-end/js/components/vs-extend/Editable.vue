<template>
    <div class="wrapper">
        <slot></slot>
        <vs-buttons
            @click="action"
            v-if="editable"
            size="sm"
            :disabled="loading"
            class="btn-action">
            {{ buttonText }}
        </vs-buttons>
    </div>
</template>

<style scoped>
    div.wrapper {
        position: relative;
    }

    span.btn-action {
        position: absolute;
        top: -1rem;
        right: 0;
    }
</style>

<script>
    const TYPE_MAP = {
        text: 'vs-form-input',
        textarea: 'vs-form-textarea'
    }

    export default {
        data: () => ({
            editing: false,
            loading: false,
            editElements: [],
            inputElements: []
        }),
        computed: {
            buttonText () {
                return this.editing ? '保存' : '编辑'
            }
        },
        watch: {
            editing (newValue) {
                jQuery(this.editElements).toggle(!newValue)
            },
            editable (newValue) {
                if (!newValue && this.editing) 
                    this.editing = false
            }
        },
        props: {
            options: {
                type: Object,
                default: () => ({})
            },
            editable: {
                type: Boolean,
                default: true
            },
            model: {
                type: Object,
                required: true,
                twoWay: true
            },
            saveAction: {
                type: Object,
                default: () => ({
                    url: '',
                    method: '',
                    dropArray: true
                })
            }
        },
        methods: {
            init () {
                this.editElements = []
                this.getEditElements(this.$el, this.editElements)
                _.forEach(this.editElements, this.initElement)
            },
            initElement ($element) {
                let type = TYPE_MAP[$element._option.type || 'text']
                let modelPath = $element._editableName
                let className = $element.className

                let $input = jQuery(`<${type}
                    size="sm"
                    class="${className}"
                    type="text"
                    v-show="editing"
                    :model.sync="model.${modelPath}">
                </${type}>`)
                jQuery($element).after($input)
                $input.hide()

                let inputElement = $input.get(0)
                this.inputElements.push(inputElement)
                this.$compile(inputElement)
            },
            getEditElements (parent, results) {
                _.forEach(parent.children, child => {
                    let attr
                    if (attr = _.find(child.attributes, { name: 'edit' })) {
                        child._editableName = attr.value
                        child._option = this.options[attr.value] || {}
                        results.push(child)
                    }
                    else
                        this.getEditElements(child, results)
                })
            },
            action () {
                this.editing = !this.editing

                if (!this.editing && this.saveAction.url) this.save()
            },
            save () {
                let data = _.cloneDeep(this.model)
                let { url, method, dropArray } = this.saveAction

                if (dropArray)
                    _.forEach(data, (value, key) => {
                        if (_.isArray(value))
                            delete data[key]
                    })

                this.$http[method](url, data)
            }
        },
        ready () {
            this.init()
        }
    }
</script>