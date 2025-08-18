import React from 'react'

interface Props {
    title: string;
    description?: string;
    children: React.ReactNode;
    actions?: React.ReactNode;
}

export const GroupContainer = ({ title, description, children, actions }: Props) => {
    return (
        <div className='flex flex-col gap-3 rounded-lg w-full bg-white'>
            <div className='flex justify-between items-center'>
                <h3 className='text-2xl text-black font-medium'>{title}</h3>
                <div>{actions}</div>
            </div>
            {description && <p className='text-sm text-gray-500'>{description}</p>}
            <div className='flex flex-col gap-4 px-2'>{children}</div>
        </div>
    )
}

export default GroupContainer;
