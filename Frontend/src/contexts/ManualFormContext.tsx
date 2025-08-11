import React, { createContext, useEffect, useState } from 'react'
import { buildFormGroups, flattenFields, objectGroup } from '../utils/formBuilder';
import type { ArrayGroup, Field, FormDataType, FormGroupType, Group, InputChangeEventType } from '../utils/types';

import jsonTemplate from "../utils/data_format.json";

export const ManualFormContext = createContext({
    formData: {},
    setFormData: () => React.useState,
    formGroupsArray: [],
    setFormGroupsArray: React.useState,
    handleAddField: (index: number) => { console.log(index) },
    handleAddGroup: (index: number, group: ArrayGroup) => { console.log(index, group) },
    handleChange: (e: InputChangeEventType) => { console.log(e.currentTarget) },
    populateForm: (jsonFormat: any) => { }
});

export interface ManualFormDataTypes {
    formData: FormDataType;
    setFormData: React.Dispatch<React.SetStateAction<FormDataType>>;
    formGroupsArray: FormGroupType[];
    setFormGroupsArray: React.Dispatch<React.SetStateAction<FormGroupType[]>>;
    handleAddField: (index: number) => void;
    handleAddGroup: (index: number, group: ArrayGroup) => void;
    handleChange: (e: InputChangeEventType) => void;
    populateForm: (jsonFormat: any) => void;
}

export const ManualFormContextProvider = ({ children }: { children: React.ReactElement }) => {
    const [formGroupsArray, setFormGroupsArray] = useState(buildFormGroups(jsonTemplate));
    const [formData, setFormData] = useState(flattenFields(formGroupsArray));

    const populateForm = (jsonFormat: any) => {
        const newFormGroupsArray = buildFormGroups(jsonFormat);
        setFormGroupsArray(newFormGroupsArray);
        setFormData(flattenFields(newFormGroupsArray))
    }
    const handleAddField = (index: number) => {
        console.log("handled add field", index)
        // setFormGroupsArray((prev) => {
        //     const newGroups = [...prev];
        //     newGroups[index] = {
        //         ...newGroups[index],
        //         fields: [...newGroups[index].fields, { id: Date.now(), label: "", value: "" }],
        //     };
        //     return newGroups;
        // });
    }



    const handleAddGroup = (index: number, parent_group: ArrayGroup) => {
        if(parent_group.fields.length >= 15) return;
        
        const { key, value: structure } = parent_group.structure;

        const subGroup_label = `${key}_${parent_group.fields.length + 1}`;
        const group: any | Field = objectGroup(subGroup_label, structure, "multiple");

        const newGroups = [...formGroupsArray];
        if (group.kind == "group") {
            newGroups[index].fields.push(group)
        }

        setFormGroupsArray(newGroups);
    }

    const handleChange = (e: InputChangeEventType) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const valueObject: any =
        { formData, setFormData, formGroupsArray, setFormGroupsArray, populateForm, handleAddField, handleAddGroup, handleChange }

    return <ManualFormContext.Provider value={valueObject}>
        {children}
    </ManualFormContext.Provider>
}