import styles from './Settings.module.css';
import {faGlobe, faKey} from "@fortawesome/free-solid-svg-icons";
import Input from "./comps/Input.jsx";
import Select from "./comps/Select.jsx";
import Button from "./comps/Button.jsx";

export default function Settings({onBarSelect}){

    return <div className={styles.settings} >

        <div className={styles.settings__main} >

            <Select title={'Language'} icon={faGlobe}/>
            <Input title={'API key:'} icon={faKey}/>

            <div className={styles.settings__main__check}>Test</div>


        </div>

        <Button onBarSelect={onBarSelect} title={'Save'} type={'save'}/>

    </div>

}