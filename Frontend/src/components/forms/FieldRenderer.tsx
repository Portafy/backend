import { type ChangeEvent } from "react";
import type { FieldMeta, InputDataType } from "../../utils/form/types";
import { useManualForm } from "../../contexts/ManualFormContext";
import { Input } from './Input';

interface Props {
    field: FieldMeta;
    value: InputDataType;
}

type InputChangeEventType = ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>

const FieldRenderer = ({ field, value }: Props) => {
    const { updateField } = useManualForm();

    const handleChange = ({ currentTarget }: InputChangeEventType) => {
        updateField(currentTarget.name, currentTarget.value)
    }
    return (
        <Input
            name={field.name}
            label={field.label}
            type={field.type}
            value={value}
            onChange={handleChange}
        />
    )
}

export default FieldRenderer;