interface Props {
    progress: number;
    containerClass?: string;
    className?: string;
}

const ProgressBar = ({ progress, containerClass, className }: Props) => {
    return (
        <div className={`${containerClass}`}>
            <div
                className={`h-1 ${className}`}
                style={{width : `${progress}%`}}
            />
        </div>
    );
}

export default ProgressBar;