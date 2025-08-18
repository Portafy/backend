import type { FormModel, FormDataType } from "./types";

export const buildInitialFormData = (model: FormModel): FormDataType => {
    const data: FormDataType = {};
    model.forEach((group) => {
        if (group.kind === "group") {
            group.fields.forEach((field) => {
                if (field.isArray) {
                    return field.items?.map((item, index) => {
                        return (data[`${field.name}_${index + 1}`] = item);
                    });
                }
                return (data[field.name] = "");
            });
        } else if (group.kind === "array") {
            // if no items exist populate nothing; otherwise add item fields
            group.items?.forEach((itemFields) => {
                itemFields.forEach((field) => {
                    if (field.isArray) {
                        return field.items?.map((item, index) => {
                            return (data[`${field.name}_${index + 1}`] = item);
                        });
                    }
                    return (data[field.name] = Array.isArray(data[field.name])
                        ? data[field.name]
                        : "");
                });
            });
        }
    });
    return data;
};




/**
 * Flatten/Unflatten helpers if you need to convert back to nested JSON later.
 * Keep these centralized so the app can serialize formData reliably.
 */

export const flattenToNested = (data: FormDataType): Record<string, any> => {
    // naive: reconstruct by splitting keys on _; we can customize for more robuse mapping
    const out: Record<string, any> = {};
    Object.entries(data).forEach(([key, value]) => {
        const parts = key.split("_");
        if (parts.length < 2) {
            out[key] = value;
            return;
        }

        const root = parts[0];
        out[root] = out[root] || {};

        // put the rest as nested key
        const rest = parts.slice(1).join("_");
        out[root][rest] = value;
    });
    return out;
};