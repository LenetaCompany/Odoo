/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";

patch(Many2XAutocomplete.prototype, {

    get searchSpecification() {

        // Keep existing specification
        const spec = {
            display_name: {},
            ...this.props.specification,
        };

        // ONLY add default_code for product models
        if (
            this.props.resModel === "product.product" ||
            this.props.resModel === "product.template"
        ) {
            spec.default_code = {};
        }

        return spec;
    },

});
