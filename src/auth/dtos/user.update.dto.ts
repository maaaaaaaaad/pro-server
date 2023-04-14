import { PartialType, PickType } from '@nestjs/swagger'
import { UserEntity } from '../entities/user.entity'
import { CoreOutputDto } from '../../common/dtos/core.output.dto'

export class UserUpdateInputDto extends PartialType(
  PickType(UserEntity, ['password', 'nickname']),
) {}

export type UserUpdateOutputDto = CoreOutputDto & {
  user?: UserEntity
}
