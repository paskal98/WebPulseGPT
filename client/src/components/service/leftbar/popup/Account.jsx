import styles from './Account.module.css';
import Button from "./comps/Button.jsx";

export default function Account({onBarSelect}){

    return <div className={styles.account} >

        <div className={styles.account__main} >
            <div className={styles.account__main__icon} >VL</div>
            <div className={styles.account__main__name} >Vlad Moskalenko</div>
            <div className={styles.account__main__email} >vladmail@gmail.com</div>
        </div>

        <Button onBarSelect={onBarSelect} title={'Sign Out'} type={'exit'}/>

    </div>

}