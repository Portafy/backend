import type { FormModel, FieldMeta } from "../form/types";

/**
 * Adapter maps the pure form model into UI-friendly FieldMeta with smarter type inference.
 * This is where we centralize heuristics (date, email detection etc.) so other code doesn't rely on the naming rules.
 */

const inferType = (name: string): FieldMeta["type"] => {
    const n = name.toLowerCase();
    if(n.includes("count")) return "number";
    if (n.includes("date")) return "date";
    if(n.includes("time")) return "time";
    if (n.includes("datetime")) return "datetime";
    if (n.includes("email")) return "email";
    if (n.includes("description") || n.includes("summary") || n.includes("bio"))
        return "textarea";
    return "text";
};

export const adapterModel = (model: FormModel): FormModel => {
    // Return a new model with types inferred
    return model.map((group) => ({
        ...group,
        fields: group.fields.map((f) => ({
            ...f,
            type: inferType(f.name) as FieldMeta["type"],
        })),
        // for array fields also map the field type
        items: group.items?.map((itemFields) =>
            itemFields.map((f) => ({
                ...f,
                type: inferType(f.name) as FieldMeta["type"],
            }))
        ),
    }));
};
