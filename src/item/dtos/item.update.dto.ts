import { PartialType, PickType } from '@nestjs/swagger'
import { ItemEntity } from '../entities/item.entity'

export class ItemUpdateInputDto extends PartialType(
  PickType(ItemEntity, ['pk', 'description', 'price']),
) {}
