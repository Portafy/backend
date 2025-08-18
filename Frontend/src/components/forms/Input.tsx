import type { InputDataType } from "../../utils/form/types";
import type { ChangeEvent } from "react";
import React from "react";

interface Props {
    label: string;
    name: string;
    type?: string;
    value: InputDataType;
    onChange: (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
    className?: string;
    containerClass?: string;
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
    onChange,
    className,
    containerClass,
}: Props) => {

    let InputElement = (
        <input
            type={type ?? "text"}
            id={name}
            name={name}
            value={value}
            onChange={onChange}
            className={`text-sm p-2 placeholder:text-sm placeholder:text-gray-500 rounded outline-2 outline-gray-300 focus:outline-black transition-colors} ${className}`}
        />
    );
    if (type === "textarea") {
        InputElement = (
            <textarea
                id={name}
                name={name}
                value={value}
                onChange={onChange}
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
