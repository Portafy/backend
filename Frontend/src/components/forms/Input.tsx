import React, { useContext } from "react";
import { ManualFormContext } from "../../contexts/ManualFormContext";

interface Props {
    label: string;
    name: string;
    type?: string;
    className?: string;
    containerClass?: string;
    value: string;
}

const ContainerWithLabel = ({
    name,
    label,
    containerClass,
    children,
}: {
    name: string;
    label: string;
    containerClass?: string;
    children: React.ReactElement;
}) => {
    return (
        <div className={`${containerClass} flex flex-col gap-2`}>
            <label htmlFor={name} className="text-black">
                {label}
            </label>
            {children}
        </div>
    );
};



export const Input = ({
    label,
    name,
    value,
    type = "text",
    className,
    containerClass,
}: Props) => {
    const { handleChange } = useContext(ManualFormContext);

    let InputElement = (
        <input
            type={type ?? "text"}
            id={name}
            name={name}
            value={value}
            onChange={handleChange}
            className={`text-sm p-2 placeholder:text-sm placeholder:text-gray-500 rounded outline-2 outline-gray-300 focus:outline-black transition-colors} ${className}`}
        />
    );
    if (type === "textarea") {
        InputElement = (
            <textarea
                id={name}
                name={name}
                value={value}
                onChange={handleChange}
                className={`text-sm p-2 resize-none placeholder:text-sm placeholder:text-gray-500 rounded outline-2 outline-gray-300 focus:outline-black transition-colors ${className}`}
            ></textarea>
        );
    }

    return (
        <ContainerWithLabel
            name={name}
            label={label}
            containerClass={containerClass}
        >
            {InputElement}
        </ContainerWithLabel>
    );
};
