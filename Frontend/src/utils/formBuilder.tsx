import type { Field, Group, ArrayGroup, FormGroupType } from "./form/types";

// --------------------
// Utility functions
// --------------------

import { toTitleCase } from "./form/parser";

const defineType = (field: string): Field["type"] => {
    if (field.endsWith("date")) return "date";
    if (field.endsWith("email")) return "email";
    if (field.endsWith("number")) return "number";
    if (field.endsWith("description") || field.endsWith("summary"))
        return "textarea";
    return "text";
};

export const fieldItem = (
    name: Field["name"],
    value: Field["value"],
    type?: Field["type"],
    label?: Field["label"],
): Field => ({
    name,
    label: label ? toTitleCase(label) : toTitleCase(name),
    type: type ?? "text",
    value,
});

const stringField = (field_name: string, value: string, label?: string): Field => {
    const input_type = defineType(field_name);
    return fieldItem(field_name, value, input_type, label);
};

const ArrayField = (field_name: string, values: string[], label?: string): Field[] =>
    values.map((item, index) => stringField(`${field_name}_${index + 1}`, item, `${label}-${index + 1}`));


export const flattenFields = (groups: FormGroupType[]) => {
    const result: Record<string, Field["value"]> = {};
    for (const group of groups) {
        if (group.kind === "group") {
            for (const field of group.fields) {
                result[field.name] = field.value;
            }
        } else if (group.kind === "array_group") {
            for (const subGroup of group.fields) {
                for (const field of subGroup.fields) {
                    result[field.name] = field.value;
                }
            }
        }
    }
    return result;
};

// --------------------
// Group builders
// --------------------

export const stringGroup = (key: string, value: string): Group => {
    return {
        kind: "group",
        group_label: toTitleCase(key),
        fields: [stringField(key, value)],
    };
};

export const objectGroup = (
    key: string,
    value: Record<string, string | string[]>,
    listing_type: string = "single"
): Group => {
    const fields: Field[] = Object.keys(value)
        .flatMap((field) => {
            const field_name: string =
                listing_type === "single" ? field : `${key}_${field}`;

            if (typeof value[field] === "string")
                return stringField(field_name, value[field] as string, field);
            if (Array.isArray(value[field]))
                return ArrayField(field_name, value[field] as string[], field);
            return undefined;
        })
        .filter((f): f is Field => f !== undefined);

    return {
        kind: "group",
        group_label: toTitleCase(key),
        fields: fields,
    };
};

export const arrayGroup = (
    key: string,
    values: Array<Record<string, string | string[]>>
): ArrayGroup => {
    return {
        kind: "array_group",
        group_label: toTitleCase(key),
        fields: values.map((value, index) =>
            objectGroup(`${key}_${index + 1}`, value, "multiple")
        ),
        structure: { key, value: values[0] }
    };
};

// --------------------
// Main builder
// --------------------

export const buildFormGroups = (json: Record<string, any>): FormGroupType[] => {
    const groups: FormGroupType[] = [];

    Object.entries(json).forEach(([key, value]) => {
        if (key.startsWith("has_")) return; // skipping group data existence indicators

        if (typeof value === "string") {
            groups.push(stringGroup(key, value));
        }
        else if (Array.isArray(value)) {
            groups.push(arrayGroup(key, value));
        }
        else if (value !== null) {
            groups.push(objectGroup(key, value));
        }
    });

    return groups;
};