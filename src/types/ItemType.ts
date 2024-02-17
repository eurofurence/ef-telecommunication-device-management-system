/**
 * Definition of all metadata associated with ItemTypes
 */
export type ItemTypeMetadata = {
    key: string;
    label: string;
    icon: string;
}

/**
 * All available item types
 */
export class ItemType {

    public static RadioDevice: ItemTypeMetadata = {
        key: 'RadioDevice',
        label: 'Radio',
        icon: 'mdi-cellphone-basic',
    };

    public static RadioAccessory: ItemTypeMetadata = {
        key: 'RadioAccessory',
        label: 'Radio Accessory',
        icon: 'mdi-headset'
    };

    public static Pager: ItemTypeMetadata = {
        key: 'Pager',
        label: 'Pager',
        icon: 'mdi-bell-ring-outline'
    };

    public static Phone: ItemTypeMetadata = {
        key: 'Phone',
        label: 'Phone',
        icon: 'mdi-phone'
    };

    public static Callbox: ItemTypeMetadata = {
        key: 'Callbox',
        label: 'Callbox',
        icon: 'mdi-webcam'
    };

    /**
     * Retrieves all available item types
     */
    public static getAll(): ItemTypeMetadata[] {
        return [
            ItemType.RadioDevice,
            ItemType.RadioAccessory,
            ItemType.Pager,
            ItemType.Phone,
            ItemType.Callbox
        ];
    }

}

