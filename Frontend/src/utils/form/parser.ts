import type { FormModel, FieldMeta } from "./types";
/**
 * Turn the JSON schema into a *pure form model* (no UI-specific heuristics).
 * This parser is intentionally conservative: it doesn't try to guess beyond "string" or "array of strings".
 */

export const parserSchema = (json: Record<string, any>): FormModel => {
    const groups: FormModel = [];
    Object.entries(json).forEach(([key, value]) => {
        if (key.startsWith("has_")) return; // skip flags

        if (typeof value === "string") {
            groups.push({
                key,
                label: toTitleCase(key),
                kind: "group",
                fields: [createFieldMeta(key, key, "text")],
            });
        } else if (Array.isArray(value)) {
            // array of objects: use first element as structure or empty place holder
            const itemStructure = value[0] ?? {};
            const fields = Object.keys(itemStructure).flatMap((f) => {
                const val = itemStructure[f];

                if (Array.isArray(val))
                    return createFieldMeta(`${key}_${f}`, f, "array", [...val]);
                return createFieldMeta(`${key}_${f}`, f, val);
            });

            groups.push({
                key,
                label: toTitleCase(key),
                kind: "array",
                fields,
                items: value.map((item, index) => {
                    return Object.entries(item).map(([field, value]) => {
                        if (Array.isArray(value)) {
                            return createFieldMeta(
                                `${key}_${index + 1}_${field}`,
                                field,
                                Array.isArray(value) ? "array" : "text",
                                [...value]
                            );
                        }
                        return createFieldMeta(
                            `${key}_${index + 1}_${field}`,
                            field,
                            Array.isArray(value) ? "array" : "text"
                        );
                    });
                }),
            });
        } else if (value && typeof value === "object") {
            const fields: FieldMeta[] = Object.keys(value).map((field) => {
                const val = value[field];
                if (Array.isArray(val))
                    return createFieldMeta(`${key}_${field}`, field, "array", [
                        ...val,
                    ]);
                return createFieldMeta(`${key}_${field}`, field, "text");
            });

            groups.push({
                key,
                label: toTitleCase(key),
                kind: "group",
                fields,
            });
        }
    });

    return groups;
};

// utitlity functions

const createFieldMeta = (
    name: string,
    label: string,
    type: FieldMeta["type"],
    items: FieldMeta["items"] = undefined
): FieldMeta => {
    return {
        name,
        label: toTitleCase(label),
        type,
        isArray: type === "array",
        items,
    };
};

export const toTitleCase = (s: string) => {
    return s.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
};
