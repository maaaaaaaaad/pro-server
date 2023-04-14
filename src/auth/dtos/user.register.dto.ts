import { PickType } from '@nestjs/swagger'
import { UserEntity } from '../entities/user.entity'
import { CoreOutputDto } from '../../common/dtos/core.output.dto'

export class UserRegisterInputDto extends PickType(UserEntity, [
  'email',
  'password',
  'nickname',
  'avatarImage',
  'social',
]) {}

export type UserRegisterOutputDto = CoreOutputDto & {
  token?: string
}
