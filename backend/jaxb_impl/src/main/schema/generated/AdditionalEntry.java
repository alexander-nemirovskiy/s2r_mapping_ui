
package generated;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.CollapsedStringAdapter;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;


/**
 * <p>Java class for AdditionalEntry complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="AdditionalEntry">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="key" type="{http://domainmodel.pts_fsm.org/2015/10/29/common}StringLength0to255"/>
 *         &lt;element name="valuetype" type="{http://domainmodel.pts_fsm.org/2015/10/29/common}MasterData.GUID" minOccurs="0"/>
 *         &lt;element name="value" type="{http://domainmodel.pts_fsm.org/2015/10/29/common}GenericTextMessage"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "AdditionalEntry", propOrder = {
    "key",
    "valuetype",
    "value"
})
public class AdditionalEntry {

    @XmlElement(required = true)
    protected String key;
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
    protected String valuetype;
    @XmlElement(required = true)
    protected GenericTextMessage value;

    /**
     * Gets the value of the key property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getKey() {
        return key;
    }

    /**
     * Sets the value of the key property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setKey(String value) {
        this.key = value;
    }

    /**
     * Gets the value of the valuetype property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getValuetype() {
        return valuetype;
    }

    /**
     * Sets the value of the valuetype property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setValuetype(String value) {
        this.valuetype = value;
    }

    /**
     * Gets the value of the value property.
     * 
     * @return
     *     possible object is
     *     {@link GenericTextMessage }
     *     
     */
    public GenericTextMessage getValue() {
        return value;
    }

    /**
     * Sets the value of the value property.
     * 
     * @param value
     *     allowed object is
     *     {@link GenericTextMessage }
     *     
     */
    public void setValue(GenericTextMessage value) {
        this.value = value;
    }

}
