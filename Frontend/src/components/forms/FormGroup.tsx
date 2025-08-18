import type { FieldMeta, FormDataType, GroupModel } from "../../utils/form/types";
import FieldRenderer from "./FieldRenderer";
interface Props {
    group: GroupModel;
    formData: FormDataType;
}

const ArrayField = ({ field }: { field: FieldMeta }) => {

    return (
        <div className="flex flex-col gap-2 py-2">
            <h1 className="text-black font-medium">{field.label}</h1>
            <div className="flex flex-col gap-2 px-2">
                {field.items?.map((item, index)=>{
                    const newField = {...field, name : `${field.name}_${index+1}`,label : `${field.label} ${index + 1}`};
                    return <FieldRenderer key={index} field={newField} value={"item"}/>
                })}
            </div>
        </div>
    )
}

export const FormGroup = ({ group, formData }: Props) => {
    return (
        <>
            {group.kind === "group" &&
                group.fields.map((field) => {
                    if (field.isArray) {
                        return <ArrayField key={field.name} field={field} />
                    }

                    return (
                        <FieldRenderer
                            key={field.name}
                            field={field}
                            value={
                                (formData[field.name] as string) ??
                                ""
                            }
                        />
                    );
                })
            }
        </>
    )
}

export const ArrayFormGroup = ({ group, formData }: Props) => {
    return (
        <>
            {(group.kind === "array" &&
                group.items?.map((item, index) => {
                    return (
                        <div
                            key={index}
                            className="flex flex-col gap-2 rounded-lg p-2 "
                        >
                            <h1 className="font-medium text-lg">{`${group.label} ${index + 1}`}</h1>
                            <div className="flex flex-col gap-4 px-4">
                                {item.map((field) => {
                                    console.log(field)
                                    if(field.isArray){
                                        return <ArrayField key={field.name} field={field}/>
                                    }
                                    return (
                                        <FieldRenderer
                                            key={field.name}
                                            field={field}
                                            value={
                                                (formData[
                                                    field.name
                                                ] as string) ?? ""
                                            }
                                        />
                                    );
                                })}
                            </div>
                        </div>
                    );
                }))}</>
    )
};