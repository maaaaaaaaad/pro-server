import { PickType } from '@nestjs/swagger'
import { ItemUpdateInputDto } from './item.update.dto'

export class ItemDeleteInputDto extends PickType(ItemUpdateInputDto, ['pk']) {}
