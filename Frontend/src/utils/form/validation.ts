import type { FieldMeta, FormValueDataType } from "./types";

export const validateField = (field : FieldMeta, value : FormValueDataType): string | null =>{
    if (field.required && value === "" || value === null || value === undefined) {
        return `${field.label} is required`;
    }
    if (field.type === "email" && value) {
        const re = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
        if(!re.test(String(value).toLowerCase())) return "Invalid email address";
    }
    // add more validation rules here 
    return null;
}