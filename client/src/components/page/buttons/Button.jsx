import styles from './Button.module.css'

export default function Button({title, spec_style="sign_in_up",onClickButton}) {

    return <>

        <button onClick={()=>onClickButton(spec_style)} className={`${styles.button} ${spec_style}`} >
            {title}
        </button>

    </>

}