import type { ChangeEvent } from "react"
export type InputChangeEventType = ChangeEvent<HTMLInputElement> | ChangeEvent<HTMLTextAreaElement>

export interface Field {
    name: string;
    label: string;
    value: string | number | boolean | null;
    type?: "text" | "number" | "date" | "email" | "textarea";
}

export type FormDataType = Record<string, string | number | boolean | null>;

export interface Group {
    kind: "group";
    group_label: string;
    fields: Field[];
}

export interface ArrayGroup {
    kind: "array_group";
    group_label: string;
    fields: Group[];
    structure : {key : string; value : Record<string, string | string[]>};
}

export type FormGroupType = Group | ArrayGroup;