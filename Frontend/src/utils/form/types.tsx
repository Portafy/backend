export type FieldType = "text" | "number" | "date" | "email" | "textarea" | "array" | "select" | "datetime" | "time";

export type InputDataType = string | number | readonly string[];

export type FormValueDataType = InputDataType | boolean | null;
export type FormDataType = Record<string, FormValueDataType>;

export interface FieldMeta {
    name: string;
    label: string;
    type?: FieldType;
    isArray? : boolean;
    items?: string[]; // for array fields
    hint?: string;
    options? : string[]; // for select or enum
    required? : boolean;
    placeholder?: string;

}

export interface GroupModel {
    key : string; // original key in the json
    label : string; // group label
    kind : "group" | "array";
    fields : FieldMeta[];  // for array groups fields represent one item structure but names are parametric
    items? : FieldMeta[][]; // only for array groups: actual existing items with concrete field names
}

export type FormModel = GroupModel[];


// export interface Group {
//     kind: "group";
//     group_label: string;
//     fields: Field[];
// }

// export interface ArrayGroup {
//     kind: "array_group";
//     group_label: string;
//     fields: Group[];
//     structure: { key: string; value: Record<string, InputDataType | InputDataType[]> };
// }

// export type FormGroupType = Group | ArrayGroup;