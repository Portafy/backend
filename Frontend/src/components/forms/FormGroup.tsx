import { useContext } from "react";
import type {
    ArrayGroup,
    Field,
    Group,
} from "../../utils/types";

import { Input } from "./Input";
import { ManualFormContext } from "../../contexts/ManualFormContext";

interface FormGroupProps {
    group: Group;
    index: number;
    data: any;
}

interface GroupFormGroupProps {
    group: ArrayGroup;
    index: number;
    data: any;
}

export const GroupFomGroup = ({ group, index, data }: GroupFormGroupProps) => {
    const { handleAddGroup } = useContext(ManualFormContext);

    const renderInput = (field: Field, index: number) => (
        <Input
            key={index}
            name={field.name}
            label={field.label}
            type={field.type}
            value={data[field.name] ?? ""}
        />
    );

    return (
        <div className="flex flex-col gap-2 rounded-lg w-full">
            <h3 className="flex justify-between items-center gap-2 text-2xl text-black font-medium">
                <span>{group?.group_label}</span>
                <span
                    className="text-xs outline-2 bg-black text-white px-4 py-2 rounded-lg cursor-pointer"
                    onClick={() => handleAddGroup(index, group)}>Add Field</span>
            </h3>
            <p className="text-sm text-gray-500">
                Please provide your list of {group.group_label.toLowerCase()}.
            </p>
            <div className="flex flex-col gap-4">
                {group.fields.map((subGroup, index) => (
                    <div key={index} className="flex flex-col gap-4 p-2 rounded-lg w-full">
                        <h3 className="text text-gray-600 font-normal">
                            {subGroup?.group_label}
                        </h3>
                        <div className="flex flex-col gap-4 px-3">
                            {subGroup.fields.map((field, index) => {
                                return renderInput(field, index);
                            })}
                        </div>
                    </div>
                ))}
            </div>
        </div>

    );
};

export const FormGroup = ({ group, index, data }: FormGroupProps) => {
    const renderInput = (field: Field, index: number) => (
        <Input
            key={index}
            name={field.name}
            label={field.label}
            type={field.type}
            value={data[field.name] ?? ""}
        />
    );

    return (
        <div className="flex flex-col gap-2 rounded-lg w-full">
            <h3 className="text-2xl text-black font-medium">
                {group?.group_label}
            </h3>
            <p className="text-sm text-gray-500">
                Please provide your {group.group_label.toLowerCase()}.
            </p>
            <div className="flex flex-col gap-4">
                {group.fields.map((field, index) => {
                    return renderInput(field, index);
                })}
            </div>
        </div>
    );
};
