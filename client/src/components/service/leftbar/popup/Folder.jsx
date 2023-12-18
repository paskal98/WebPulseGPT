import styles from './Folder.module.css';
import {faFolder} from "@fortawesome/free-solid-svg-icons";
import Input from "./comps/Input.jsx";
import Button from "./comps/Button.jsx";

export default function Folder({onBarSelect}){

    return <div className={styles.folder} >

        <div className={styles.folder__main} >

            <Input title={'Folder Name'} icon={faFolder}/>

        </div>

        <Button onBarSelect={onBarSelect} title={'Save'} type={'save'}/>

    </div>

}