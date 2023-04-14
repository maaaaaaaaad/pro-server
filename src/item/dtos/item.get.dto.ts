import { PickType } from '@nestjs/swagger'
import { ItemEntity } from '../entities/item.entity'

export class ItemGetInputDto extends PickType(ItemEntity, ['pk']) {}
