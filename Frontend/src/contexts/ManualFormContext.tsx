import React, { createContext, useContext, useMemo, useState } from 'react'
import type { FormValueDataType, FormDataType, FormModel, GroupModel, FieldMeta } from '../utils/form/types';

import { parserSchema } from '../utils/form/parser';
import { adapterModel } from '../utils/form/adapter';
import { buildInitialFormData } from '../utils/form/formUtils';
import schema from "../components/schema/data_format.json"

export interface ManualFormContextType {
    model: FormModel;
    formData: FormDataType;
    setFormData: (updater: (prev: FormDataType) => FormDataType) => void;
    addGroup: (groupKey: string) => void;
    updateField: (name: string, value: FormValueDataType) => void;
    populate: (json: Record<string, any>) => void;
}
export const ManualFormContext = createContext<ManualFormContextType | undefined>({
    model: {} as FormModel,
    formData: {} as FormDataType,
    setFormData: () => { },
    addGroup: () => { },
    updateField: () => { },
    populate: () => { }
});

export const ManualFormContextProvider = ({ children }: { children: React.ReactNode }) => {
    console.log(parserSchema(schema as any))
    const baseModel = useMemo(() => adapterModel(parserSchema(schema as any)), []);
    const [model, setModel] = useState<FormModel>(baseModel);
    const [formData, setFormDataState] = useState<FormDataType>(() => buildInitialFormData(baseModel));

    type updaterType = (prev: FormDataType) => FormDataType;
    const setFormData = (updater: updaterType) => {
        return setFormDataState(prev => updater(prev));
    }

    const updateField = (name: string, value: FormValueDataType) => {
        setFormDataState((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const addGroup = (groupKey: string) => {
        const newModel: FormModel = model.map(group => {
            if (group.key !== groupKey || group.kind !== "array") return group;

            const newItem = createNewSubGroup(group);
            group.items ? group.items.push(newItem) : group.items = [newItem];
            return group;
        })

        console.log(newModel)
        setModel(newModel);
    }
    
    const populate = (json: Record<string, any>) => {
        const newModel = adapterModel(parserSchema(json));
        setModel(newModel);
        console.log({newModel})
        setFormData((_) => buildInitialFormData(newModel));
    }

    return <ManualFormContext.Provider value={{
        model,
        formData,
        setFormData,
        addGroup,
        updateField,
        populate,
    }}>
        {children}
    </ManualFormContext.Provider>
}

export const useManualForm = () => {
    const context = useContext(ManualFormContext);
    if (!context) throw new Error("useManualForm must be used within a ManualFormContextProvider");
    return context;
}


// utility functions
const createNewSubGroup = (group: GroupModel): FieldMeta[] => {
    const itemsCount = group.items?.length ?? 0;

    const groupStructure = group.fields.map(f => (
        { ...f, name: f.name.split("_").slice(1).join("_") }
    ));

    const newItem: FieldMeta[] = groupStructure.map(f => (
        { ...f, name: `${group.key}_${itemsCount + 1}_${f.name}` }
    ))

    return newItem;
}